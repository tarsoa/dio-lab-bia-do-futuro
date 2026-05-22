# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Valor esperado de R$ 570,00 baseado no `transacoes.csv`
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Formulário de Feedback

Use com os participantes do teste:

| Métrica | Pergunta | Nota (1-5) |
|---------|----------|------------|
| Assertividade | "A resposta respondeu sua pergunta? | 4 |
| Segurança | " As informações pareceram confiáveis | 4 |
| Coerência | " A linguagem foi clara e fácil de entender?" | 5 |

**Comentário aberto:** O que poderia melhorar? 
---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- A aplicação depois de algumas alterações nas regras funcionou dentro do System Prompt proposto.

**O que pode melhorar:**
- Durante a execução do desafio notei que a arquitetura proposta com Ollama local apresentava gargalos de hardware e latência no tempo de resposta para o usuário. Como oportunidade de melhoria, decidi modernizar o projeto migrando o "cérebro do agente" para a nuvem através da API oficial do Google com o Gemini 2.5 Flash. Com isso, consegui otimizar o desempenho da aplicação, aplicando boas práticas com o gerenciamento seguro de chaves de API via variáveis de ambiente garantindo respostas imediatas de qualidade.

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da sua solução, como:

- Latência e tempo de resposta: Com a migração da infraestrutura local do Ollama para a API em nuvem do Gemini 2.5 Flash, a latência foi drasticamente reduzida. O tempo de resposta, que antes dependia do processamento e do hardware da minha máquina local, passou a ser processado imediatamente pelos servidores do Google, garantindo uma experiência de chat fluida e em tempo real para o usuário final.

- Consumo de tokens e custos: Para a execução da aplicação, optei por utilizar o modelo Gemini 2.5 Flash dentro da camada gratuita (Free Tier) do Google AI Studio. Essa escolha me permitiu testar a aplicação sem custos financeiros, respeitando o limite de 15 requisições por minuto e 1.500 requisições diárias. O controle de consumo de tokens pode ser monitorado diretamente pelo painel de controle do Google AI Studio Cloud.
  
- Logs e taxa de erros: A aplicação foi blindada utilizando estruturas de tratamento de exceções (try/except) no Python. Caso ocorra alguma falha na comunicação ou estouro de cota com a API do Google (como o erro de limite de requisições 429 RESOURCE_EXHAUSTED), o sistema captura o erro imediatamente e exibe uma mensagem amigável na tela, impedindo que a interface do Streamlit trave e gerando o log da falha diretamente no console para diagnóstico.

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento. Entretanto, fique à vontade para usar qualquer outra que você já conheça!
