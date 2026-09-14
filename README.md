# NFe Validator — Validador/Parser de Notas Fiscais

## 1. Visão Geral

Este projeto implementa um serviço que recebe dados estruturados de uma Nota
Fiscal (JSON) e os valida contra um conjunto de regras de negócio (campos
obrigatórios, formatos, faixas de valores e cálculo de impostos). O objetivo
não é substituir a validação oficial da SEFAZ, e sim simular, em escopo
reduzido e didático, um motor de regras de negócio testável — usado aqui como
estudo de caso para o fluxo **SDD (Spec-Driven Development)**.

O desenvolvimento seguiu o fluxo:

```
Especificação (SPEC.md) → Geração assistida por IA (Claude Code) → Testes → Refinamento da spec → Nova geração
```

## 2. Arquitetura (resumo)

```
nfe-validator/
├── SPEC.md                  # Especificação técnica (fonte da verdade)
├── docs/
│   └── ADR.md                # Registro de decisões arquiteturais
├── .claude/
│   └── CLAUDE.md              # Regras/contexto dados ao agente de IA
├── src/nfe_validator/
│   ├── models.py              # Estruturas de dados (NotaFiscal, Item, etc.)
│   └── validator.py           # Motor de regras de validação
├── tests/
│   └── test_validator.py      # Suíte de testes (casos normais + edge cases)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Ver `docs/ADR.md` para o racional de cada decisão técnica.

## 3. Como instalar e executar

### Opção A — Docker (recomendado, ambiente padronizado)

```bash
docker compose build
docker compose run --rm app pytest -v
```

### Opção B — Localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

### Rodando o validador manualmente

```bash
python -m nfe_validator.cli exemplos/nota_valida.json
```

## 4. Fluxo de trabalho do time (governança)

- `main`: código estável, protegido (merge apenas via Pull Request aprovado).
- `develop`: integração das features antes de ir para `main`.
- `feature/<nome-da-tarefa>`: uma branch por tarefa/issue.
- Toda tarefa é uma Issue vinculada ao GitHub Project (quadro Kanban).
- Todo merge exige ao menos 1 revisão (Pull Request Review) de outro membro.

## 5. Agentes de IA utilizados

- **Ferramenta:** Claude Code, orientado pelas regras em `.claude/CLAUDE.md`.
- **Uso documentado:** o agente foi usado para (a) gerar o esqueleto do
  módulo `validator.py` a partir da `SPEC.md`, (b) gerar casos de teste a
  partir das regras de negócio descritas na especificação, e (c) revisar
  edge cases não cobertos originalmente na spec (ver seção "Refinamento" em
  `SPEC.md`).

## 6. Registro Sintético de Decisões Arquiteturais (ADR)

Ver detalhes completos em `docs/ADR.md`. Resumo:

| ADR | Decisão | Motivo |
|-----|---------|--------|
| 001 | Python + pytest | Simplicidade, rapidez de escrita de testes, boa integração com agentes de IA |
| 002 | Regras de negócio como funções puras | Facilita testes unitários isolados e geração incremental via IA |
| 003 | Sem banco de dados | Escopo do problema não exige persistência; validação é stateless |
| 004 | Docker para padronização de ambiente | Garantir que "funciona na minha máquina" não seja um problema entre os membros do time |

## 7. Relatório de Execução dos Testes

Ver `docs/TEST_REPORT.md` para o log de execução mais recente da suíte de
testes (cole aqui o output de `pytest -v` depois de rodar no ambiente
padronizado, com print/screenshot como evidência).

## 8. Equipe

| Nome completo | RA |
|---------------|----|
| Miguel Henrique Araujo Dutra | 22306726|

