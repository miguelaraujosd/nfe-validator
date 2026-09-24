# ADR 006 — Adoção formal do fluxo SDD com homologação humana obrigatória

**Contexto:** a Entrega 2 exige defesa explícita das decisões de
arquitetura e evidência de que o uso de IA no ciclo de desenvolvimento
foi acompanhado de revisão humana crítica, não apenas aceito
automaticamente.

**Decisão:** todo código gerado com auxílio de agente de IA (Claude
Code) passa obrigatoriamente por: (1) validação contra a `SPEC.md`
vigente, (2) execução da suíte de testes automatizados, e (3) revisão
via Pull Request antes do merge em `develop` ou `main`. Nenhuma sugestão
do agente é incorporada diretamente à `main` sem esse ciclo.

**Consequências:** o processo fica mais lento do que aceitar sugestões
de IA diretamente, mas garante rastreabilidade e responsabilidade humana
sobre cada decisão incorporada ao produto final — trade-off considerado
necessário dado o caráter formativo da disciplina e a natureza sensível
do domínio (dados fiscais).

---

## ADR 007 — Uso do print/log estático como evidência de execução, com Docker como ambiente de referência

**Contexto:** durante o desenvolvimento, nem todos os membros do time
tinham Docker e/ou Python pré-instalados em suas máquinas, o que
dificultou a geração de evidência de execução em ambiente 100%
padronizado dentro do prazo da entrega.

**Decisão:** o `Dockerfile` e `docker-compose.yml` permanecem como
ambiente de referência oficial do projeto (é o que deve ser usado por
quem for avaliar o projeto). Quando a execução direta em Docker não foi
possível a tempo por limitação de ambiente local, o time documentou a
execução local equivalente (mesma suíte de testes, mesmo resultado) como
evidência complementar, deixando explícito no relatório qual ambiente
gerou qual evidência.

**Consequências:** transparência sobre uma limitação real de ambiente,
em vez de omitir a informação — considerado mais alinhado aos princípios
de honestidade técnica do que apresentar uma evidência não gerada de
fato.
