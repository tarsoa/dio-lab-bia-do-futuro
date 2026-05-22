import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import pandas as pd
import streamlit as st
import unicodedata
from dotenv import load_dotenv
from google import genai

# ==================== CONFIGURAÇÃO =====================
# Carrega a chave do arquivo .env que criamos na raiz
load_dotenv()

# Inicializa o cliente do Gemini usando a chave de ambiente
load_dotenv()
os.environ["PYTHONIOENCODING"] = "utf-8"
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Erro: A variável GEMINI_API_KEY não foi encontrada no arquivo .env!")
    st.stop()

client = genai.Client(api_key=api_key)

# Modelo ideal para o plano gratuito (rápido e altamente inteligente)
MODELO = "gemini-2.5-flash"

# ======================= FUNÇÕES =======================
# Função auxiliar para formatar valores em Real brasileiro
def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# =================== CARREGAR DADOS ====================
# Forçamos o encoding='utf-8' para o Python ler os acentos em português corretamente

perfil = json.load(open('./data/perfil_investidor.json', encoding='utf-8'))
transacoes = pd.read_csv('./data/transacoes.csv', encoding='utf-8')
historico = pd.read_csv('./data/historico_atendimento.csv', encoding='utf-8')

# Abrindo o JSON de produtos com a codificação correta
with open('./data/produtos_financeiros.json', encoding='utf-8') as f:
    produtos = json.load(f)

# Formatar valores do CSV para R$ brasileiro
transacoes['valor_formatado'] = transacoes['valor'].apply(formatar_brl)


# =================== MONTAR CONTEXTO ===================

# Converter transações para lista legível em vez de to_string()
transacoes_texto = "\n".join(
    f"- {row['categoria']}: {row['valor_formatado']} ({row['descricao']})"
    for _, row in transacoes.iterrows()
)

historico_texto = "\n".join(
    f"- {row['data']} ({row['canal']}): {row['tema']} — {row['resumo']}"
    for _, row in historico.iterrows()
)

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: {formatar_brl(perfil['patrimonio_total'])}
RESERVA: {formatar_brl(perfil['reserva_emergencia_atual'])}

TRANSAÇÕES RECENTES:
{transacoes_texto}

ATENDIMENTOS ANTERIORES:
{historico_texto}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, ensure_ascii=False)}

"""


# ==================== SYSTEM PROMPT ====================
SYSTEM_PROMPT = """Você é o Edu, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
- NUNCA recomende investimentos específicos - apenas explique como funcionam;
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais;
- Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo;
- Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
- NUNCA use caracteres especiais de formatação (como asteriscos de negrito **) dentro ou colados em valores monetários;
- Sempre escreva palavras com acentos de forma limpa e natural, garantindo que haja um espaço visível antes e depois de qualquer 
  valor monetário (exemplo: "gastou R$ 570,00 com alimentação" e nunca grudado como "R$570,00com").

"""

# ==================== CHAMAR GEMINI ====================
def perguntar(msg):
    conteudo_prompt = f"""
    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta do Usuário: {msg}
    """
    
    try:
        response = client.models.generate_content(
            model=MODELO,
            contents=conteudo_prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.7
            }
        )
        # Limpa asteriscos residuais que o modelo insiste em usar
        texto = unicodedata.normalize("NFKC", response.text)

        texto = texto.replace("**", "")
        texto = texto.replace("__", "")

        return texto
    except Exception as e:
        return f"Erro ao chamar a API do Gemini: {e}"


# ====================== INTERFACE ======================
st.title("🎓 Edu, Seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("Edu está pensando..."):
        resposta = perguntar(pergunta)
        
        # Escuda o cifrão para o Streamlit não inventar fórmulas matemáticas
        resposta_protegida = resposta.replace("$", r"\$")
        
        # Exibe o texto perfeitamente na tela
        st.chat_message("assistant").markdown(resposta_protegida)
