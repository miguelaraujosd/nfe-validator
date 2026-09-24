# Relato de Experiência — Desenvolvimento em Grupo

## 1. Contexto do time

O grupo optou pelo problema de **Validador/Parser de Notas Fiscais** por
oferecer um bom equilíbrio entre riqueza de regras de negócio e baixa
complexidade de infraestrutura, permitindo focar o esforço no processo
de Spec-Driven Development (SDD) e na governança do repositório, em vez
de gastar tempo com configuração de banco de dados ou autenticação.

## 2. O que funcionou bem

- **Escrever a especificação antes do código** evitou retrabalho: as
  regras de negócio (RN01–RN05) já estavam claras antes de qualquer
  linha de código ser gerada, o que tornou a geração assistida por IA
  mais previsível e alinhada ao que o time realmente precisava.
- **Usar o agente de IA (Claude Code) como acelerador, não como autor
  único**: o agente gerou o esqueleto do código e da suíte de testes,
  mas cada regra de negócio foi conferida manualmente contra a `SPEC.md`
  antes de ser aceita.
- **Governança de branches** (main protegida, develop, feature/*) deixou
  claro qual código estava "pronto para produção" e qual ainda estava em
  desenvolvimento, mesmo em uma equipe pequena.

## 3. Desafios encontrados

- **Ambiente de desenvolvimento heterogêneo**: nem todas as máquinas do
  time tinham Python ou Docker instalados previamente, o que reforçou a
  importância de documentar comandos de instalação passo a passo no
  README e de fornecer um `Dockerfile` como ambiente de fallback
  padronizado.
- **Erros silenciosos de ponto flutuante**: a suíte de testes revelou um
  bug real (diferença de R$ 0,01 sendo rejeitada por erro de
  arredondamento binário) que não havia sido previsto na especificação
  original — só foi descoberto ao *rodar* os testes, não ao escrevê-los,
  reforçando o valor do ciclo teste → correção → re-especificação.
- **Coordenação de Git em equipe reduzida**: com poucos integrantes
  ativos simultaneamente, o processo de revisão por pares (code review)
  precisou ser adaptado — critérios de aceitação foram documentados
  previamente para que a revisão pudesse ser objetiva mesmo quando feita
  de forma assíncrona.

## 4. Aprendizados

- Uma especificação escrita antes do código funciona como um "contrato"
  entre o time e o agente de IA: qualquer ambiguidade encontrada durante
  a implementação foi tratada como uma falha da especificação, não uma
  decisão livre de implementação — isso manteve o código rastreável às
  regras de negócio documentadas.
- Testes automatizados não são apenas uma etapa de validação final: eles
  atuaram como uma ferramenta de **descoberta de requisitos ausentes**
  (o caso da RN03 — limite de valor alto — só foi adicionado à spec
  depois que o time percebeu, ao escrever os testes de borda, que não
  havia regra nenhuma tratando notas de valor muito elevado).
- Revisão humana continua sendo indispensável mesmo com uso de IA: o
  agente gerou código sintaticamente correto em todos os casos, mas as
  decisões de *quais* regras implementar e *como* interpretar zonas
  cinzentas da especificação (ex: tolerância de arredondamento) exigiram
  julgamento humano.
