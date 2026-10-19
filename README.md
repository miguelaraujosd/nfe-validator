# NFe Validator — Validador/Parser de Notas Fiscais

Versão **v1.0.0** · Python 3.11 · 40 testes · 99% de cobertura

Serviço (via linha de comando) que recebe uma Nota Fiscal em JSON e valida
contra regras de negócio: campos obrigatórios, CPF/CNPJ, cálculo de total e
ICMS, limite de valor e data de emissão. Desenvolvido com o fluxo
**Spec-Driven Development (SDD)** usando o Claude Code como agente de apoio.
Não substitui a validação oficial da SEFAZ; é um estudo de caso didático.

## Início rápido

### Opção A — Docker (ambiente padronizado, comando único)

```bash
docker compose up --build test
```

Sobe o ambiente, executa os 40 testes e imprime o relatório de cobertura.

Para validar uma nota:

```bash
docker compose run --rm app exemplos/nota_valida.json
docker compose run --rm app exemplos/nota_cpf_invalido.json
```

### Opção B — Local (sem Docker)

Requisitos: Python 3.11 ou superior.

```bash
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Linux/macOS:           source .venv/bin/activate
pip install -r requirements.txt
```

Variável de ambiente necessária (apenas indica onde está o código-fonte):

```bash
# Windows (PowerShell):  $env:PYTHONPATH = "src"
# Linux/macOS:           export PYTHONPATH=src
```

Executar os testes com cobertura:

```bash
pytest -v --cov=src/nfe_validator --cov-report=term-missing
```

Validar uma nota pelo CLI (no Windows, o comando pode ser `py` em vez de `python`):

```bash
python -m nfe_validator.cli exemplos/nota_valida.json
```

O programa imprime o resultado em JSON e encerra com código `0` (nota válida)
ou `1` (nota inválida).

## Configuração

O projeto não usa credenciais, chaves de API nem banco de dados. A única
variável de ambiente é `PYTHONPATH=src`, já definida no `Dockerfile` e no
`docker-compose.yml`.

## Arquitetura

```
src/nfe_validator/
├── models.py     estruturas de dados (dataclasses)
├── validator.py  regras de negócio (funções puras)
└── cli.py        interface de linha de comando
```

Fluxo da aplicação (detalhes em [`docs/DIAGRAMA_FLUXO.md`](docs/DIAGRAMA_FLUXO.md)):

```
JSON da nota -> campos obrigatórios -> cálculo de totais -> regras RN01/RN03/RN04/RN05 -> resultado {valido, erros, valor_calculado, icms_total}
```

## Documentação

| Documento | Conteúdo |
|---|---|
| [`SPEC.md`](SPEC.md) | Especificação de trabalho (Entregas 1 e 2) |
| [`docs/SPEC_AS_BUILT.md`](docs/SPEC_AS_BUILT.md) | Especificação definitiva (As-Built) da v1.0.0 |
| [`docs/ADR.md`](docs/ADR.md), [`docs/ADR_ADICIONAL.md`](docs/ADR_ADICIONAL.md) | Decisões de arquitetura |
| [`docs/TEST_REPORT.md`](docs/TEST_REPORT.md) | Histórico de testes e bug de arredondamento corrigido |
| [`docs/COVERAGE_REPORT.md`](docs/COVERAGE_REPORT.md) | Relatório de cobertura (99%) |
| [`docs/ANALISE_IA.md`](docs/ANALISE_IA.md) | Comparativo de ferramentas de IA e análise ética |
| [`docs/RELATO_EXPERIENCIA.md`](docs/RELATO_EXPERIENCIA.md) | Relato de experiência do grupo |
| [`docs/RETROSPECTIVA_FINAL.md`](docs/RETROSPECTIVA_FINAL.md) | Retrospectiva e lições aprendidas |

## Governança

- `main`: protegida, só recebe código via Pull Request.
- `develop`: integração. `feature/*`: uma branch por tarefa.
- Tarefas registradas como Issues e organizadas no GitHub Projects (board Kanban).
- Instruções de contexto do agente de IA: [`.claude/CLAUDE.md`](.claude/CLAUDE.md).

## Equipe

| Nome completo | RA |
|---|---|
| Miguel Henrique Araujo Dutra | 22306726 |
| (adicionar demais integrantes) | |
