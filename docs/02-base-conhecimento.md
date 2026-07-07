# 02 — Base de Conhecimento

## Objetivo da Base

A base de conhecimento do FitGuia IA organiza as informações usadas pelo agente para responder com mais precisão.

Ela é composta por quatro arquivos principais:

```text
data/
├── perfil_usuario.json
├── exercicios.csv
├── historico_atendimento.csv
└── base_conhecimento_treino.json
```

## Arquivo: perfil_usuario.json

Contém um perfil simulado de pessoa usuária. Esse arquivo permite que o agente personalize exemplos sem depender de dados reais.

Campos principais:

- Nome;
- Idade;
- Objetivo principal;
- Ambiente preferido;
- Nível;
- Tempo disponível;
- Equipamentos disponíveis;
- Restrições informadas.

## Arquivo: exercicios.csv

Contém exercícios organizados por:

- Nome;
- Grupo muscular;
- Ambiente;
- Equipamento;
- Nível;
- Observação técnica.

Esse arquivo ajuda o agente a sugerir exercícios compatíveis com o contexto.

## Arquivo: historico_atendimento.csv

Simula atendimentos anteriores. Ele permite que o agente use contexto histórico, como:

- Dúvidas já feitas;
- Temas recorrentes;
- Orientações anteriores;
- Se o atendimento foi resolvido.

## Arquivo: base_conhecimento_treino.json

Reúne princípios gerais sobre:

- Frequência;
- Segurança;
- Progressão;
- Treino em casa;
- Treino na academia;
- Sinais de risco;
- Limites do agente;
- Fontes abertas usadas no projeto.

## Fontes Utilizadas

### CDC — Adult Activity: An Overview

Link: https://www.cdc.gov/physical-activity-basics/guidelines/adults.html

Uso no projeto:

- Recomendação geral de atividade física para adultos;
- Fortalecimento muscular em dois ou mais dias por semana;
- Importância da regularidade.

### CDC — Physical Activity Guidelines for School-Aged Children and Adolescents

Link: https://www.cdc.gov/physical-activity-education/guidelines/index.html

Uso no projeto:

- Atividade física para jovens;
- Fortalecimento muscular e ósseo em dias específicos da semana;
- Valorização de atividades adequadas à idade.

### ACSM — Physical Activity Guidelines

Link: https://acsm.org/education-resources/trending-topics-resources/physical-activity-guidelines/

Uso no projeto:

- Reforço sobre atividade aeróbica e fortalecimento muscular;
- Regularidade;
- Construção gradual do hábito.

### ACSM — Resistance Training for Health and Fitness

Link: https://www.prescriptiontogetactive.com/static/pdfs/resistance-training-ACSM.pdf

Uso no projeto:

- Treino resistido;
- Grandes grupos musculares;
- Progressão gradual;
- Segurança em treinamento de força.

## Estratégia Anti-Alucinação

O system prompt orienta a LLM a:

1. Usar apenas o contexto fornecido;
2. Não inventar exercícios fora da base;
3. Admitir quando não houver informação suficiente;
4. Fazer perguntas antes de montar uma rotina incompleta;
5. Evitar recomendações médicas ou promessas de resultado.
