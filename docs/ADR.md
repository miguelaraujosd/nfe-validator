# ADR — Registro de Decisões Arquiteturais

## ADR 001 — Linguagem e stack de testes: Python + pytest

**Contexto:** precisávamos de uma linguagem com sintaxe simples, boa
integração com agentes de IA de geração de código, e um framework de testes
maduro.

**Decisão:** Python 3.11 + pytest.

**Consequências:** curva de aprendizado baixa para o time; grande volume de
exemplos de treino do agente de IA em Python, o que melhora a qualidade do
código gerado; pytest permite parametrização de testes, essencial para
cobrir os muitos edge cases da SPEC.md sem duplicar código.

---

## ADR 002 — Regras de negócio como funções puras, sem estado

**Contexto:** o problema (validação de nota fiscal) não exige persistência
nem histórico de execuções anteriores.

**Decisão:** cada regra de negócio (RN01–RN05) é implementada como uma
função pura: mesma entrada sempre produz a mesma saída, sem efeitos
colaterais.

**Consequências:** testabilidade máxima (nenhum mock ou fixture de banco
necessário); facilita geração incremental via IA, já que cada função pode
ser gerada e testada isoladamente a partir de um trecho específico da
SPEC.md.

---

## ADR 003 — Sem banco de dados

**Contexto:** o escopo do problema (validar uma nota recebida, retornar um
resultado) não exige guardar histórico.

**Decisão:** não incluir banco de dados nesta entrega.

**Consequências:** reduz drasticamente a superfície de infraestrutura e o
número de coisas que podem "quebrar no ambiente de outra pessoa" — alinhado
ao objetivo de manter o esforço de entrega gerenciável. Caso o time queira
evoluir o projeto depois, um ADR futuro pode reavaliar essa decisão.

---

## ADR 004 — Docker para padronização do ambiente

**Contexto:** múltiplos membros do time, múltiplas máquinas, risco de
"funciona aqui, não funciona aí".

**Decisão:** fornecer `Dockerfile` e `docker-compose.yml` que encapsulam a
versão exata do Python e das dependências.

**Consequências:** qualquer membro do time (ou o professor avaliando)
consegue rodar `docker compose run --rm app pytest -v` e obter o mesmo
resultado, independente do sistema operacional local.

---

## ADR 005 — Uso de agente de IA (Claude Code) no fluxo SDD

**Contexto:** a entrega exige orquestração documentada de um agente de
geração de código dentro de um fluxo Spec-Driven Development.

**Decisão:** a SPEC.md é escrita e revisada pelo time **antes** de qualquer
geração de código. O agente (Claude Code) recebe a SPEC.md como contexto e
gera o código e os testes a partir dela — nunca o contrário. As regras de
como o agente deve se comportar estão documentadas em `.claude/CLAUDE.md`.

**Consequências:** qualquer ambiguidade percebida durante a geração de
código ou testes é tratada como um gap na especificação, e resolvida
**editando a SPEC.md primeiro** (ver seção 7 de SPEC.md), e só depois
regenerando o código — mantendo a spec como fonte única da verdade.
