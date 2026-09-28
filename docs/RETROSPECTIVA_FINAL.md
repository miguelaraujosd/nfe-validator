# Retrospectiva Final do Projeto

## 1. Eficácia do uso de Agentes de IA no fluxo SDD

O uso do Claude Code ao longo de todo o ciclo (Entregas 1, 2 e 3) validou
a hipótese central do fluxo Spec-Driven Development: escrever a
especificação antes do código torna a geração assistida por IA mais
previsível e verificável. Em nenhum momento o agente "inventou" uma regra
de negócio não documentada — quando uma lacuna foi percebida (ex: ausência
de regra para notas de valor alto), ela foi tratada como uma atualização
de especificação, não como uma decisão livre de implementação.

## 2. Ganho de produtividade observado

- A geração do esqueleto de código (`models.py`, `validator.py`) e da
  suíte inicial de testes a partir da `SPEC.md` foi substancialmente mais
  rápida do que escrever ambos do zero manualmente.
- A correção de bugs também foi acelerada: o bug de ponto flutuante na
  RN01 foi diagnosticado e corrigido no mesmo ciclo de execução dos
  testes, sem necessidade de investigação manual extensa.
- A documentação (ADRs, relatórios de teste, specs As-Built) foi gerada e
  mantida atualizada de forma muito mais consistente do que normalmente
  ocorre em projetos onde a documentação é escrita manualmente e tende a
  ficar desatualizada.

## 3. Principais dificuldades superadas

- **Configuração de ambiente heterogêneo**: nem todas as máquinas do time
  tinham Python e Docker pré-instalados, o que atrasou a geração de
  evidências de execução em alguns momentos — resolvido documentando
  claramente os dois caminhos de instalação (Docker e local) no README.
- **Governança de Git para equipe pequena**: adaptar o processo de code
  review (Pull Request + aprovação) para um número reduzido de membros
  ativos, sem abrir mão do registro formal do fluxo de branches
  protegidas.
- **Erros sutis de lógica**: o bug de arredondamento de ponto flutuante
  reforçou que "código gerado que funciona" não é o mesmo que "código
  correto" — só os testes de borda revelaram o problema.

## 4. Lições aprendidas sobre governança em equipe

- Uma especificação técnica bem escrita antes do código funciona como
  ferramenta de alinhamento entre pessoas, não só entre humano e IA.
- Testes automatizados de borda são a forma mais confiável de descobrir
  lacunas na especificação original — o time tratou cada falha de teste
  como uma pergunta em aberto sobre a spec, não apenas como um bug a
  corrigir silenciosamente.
- Branch protection e Pull Requests obrigatórios, mesmo em equipes
  pequenas, mantêm um histórico rastreável de decisões técnicas — algo
  que se mostrou valioso ao escrever a documentação final (As-Built) e a
  análise crítica do uso de IA.
- A revisão humana permanece indispensável em cada etapa: aceitar
  código, testes e documentação gerados por IA sem verificação é o maior
  risco identificado ao longo de todo o projeto (ver `docs/ANALISE_IA.md`
  da Entrega 2 para a discussão ética completa).

## 5. Resumo executivo de encerramento

O projeto **NFe Validator** foi concluído com sucesso, cumprindo o escopo
definido na especificação original com pequenos ajustes justificados e
documentados (ver `docs/SPEC_AS_BUILT.md`, seção 8). A suíte de testes
automatizados atinge 100% de aprovação (22/22 testes) com 95% de
cobertura de código. O repositório está publicado, versionado com a tag
`v1.0.0`, e acompanhado de documentação técnica completa (especificação,
ADRs, relatórios de teste e cobertura, e análise crítica do uso de
ferramentas de IA no ciclo de desenvolvimento).
