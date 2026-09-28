# SPEC.md (As-Built) — Especificação Técnica Definitiva

Versão: 1.0.0 (Release Final)
Status: **As-Built** — reflete exatamente o que foi entregue na versão
final do software, e não mais a intenção original de projeto.

> Este documento substitui, para fins de encerramento, a SPEC.md de
> trabalho usada durante o desenvolvimento (Entregas 1 e 2). As
> diferenças entre a especificação original e esta versão final estão
> registradas na seção 8 (Divergências entre Spec Inicial e As-Built).

## 1. Escopo entregue

O sistema é um validador/parser de Notas Fiscais em formato JSON, que
recebe uma nota e retorna um veredito de validade acompanhado de uma
lista detalhada de erros (se houver), do valor total calculado e do
total de ICMS. É stateless, não possui banco de dados, não realiza
integração com SEFAZ e não possui autenticação — exatamente como
definido no escopo original.

## 2. Contrato de Entrada (Input) — confirmado como implementado

```json
{
  "numero": "000123",
  "serie": "1",
  "data_emissao": "2026-09-10",
  "emitente": { "cnpj": "12345678000199", "razao_social": "Empresa Exemplo LTDA" },
  "destinatario": { "documento": "12345678900", "nome": "Cliente Exemplo" },
  "itens": [
    { "descricao": "Produto A", "quantidade": 2, "valor_unitario": 50.00, "aliquota_icms": 0.18 }
  ],
  "valor_total_declarado": 118.00,
  "autorizacao_especial": false
}
```

Todos os campos e tipos descritos na especificação original foram
implementados sem alteração de contrato (ver `src/nfe_validator/models.py`
para as estruturas de dados exatas: `NotaFiscal`, `Emitente`,
`Destinatario`, `ItemNota`).

## 3. Contrato de Saída (Output) — confirmado como implementado

```json
{
  "valido": false,
  "erros": [
    { "campo": "valor_total_declarado", "regra": "RN01", "mensagem": "Valor declarado (118.00) difere do valor calculado (100.00)." }
  ],
  "valor_calculado": 100.00,
  "icms_total": 18.00
}
```

Implementado em `ResultadoValidacao.to_dict()` (`src/nfe_validator/models.py`).

## 4. Regras de Negócio — implementadas e testadas (100% dos casos críticos)

| Regra | Descrição | Função responsável | Cobertura de teste |
|---|---|---|---|
| RN01 | Valor declarado deve igualar valor calculado com tolerância de R$ 0,01 | `validar_regras_negocio` | 100% (inclui correção de bug de ponto flutuante) |
| RN02 | Cálculo do ICMS total por item, informativo | `calcular_totais` | 100% |
| RN03 | Notas acima de R$ 100.000,00 exigem `autorizacao_especial: true` | `validar_regras_negocio` | 100% (inclui caso-limite exato) |
| RN04 | Data de emissão não pode ser futura nem ter mais de 5 anos | `validar_regras_negocio` | 100% |
| RN05 | CPF (11 dígitos) ou CNPJ (14 dígitos) do destinatário deve ser matematicamente válido | `validar_documento` | 100% |

Todas as regras acima correspondem exatamente ao código-fonte na versão
da release `v1.0.0` — nenhuma regra adicional foi implementada além das
documentadas, e nenhuma regra documentada ficou sem implementação
correspondente.

## 5. Componentes e APIs (Arquitetura entregue)

```
src/nfe_validator/
├── models.py       → Estruturas de dados (dataclasses)
├── validator.py    → Motor de regras de negócio (funções puras)
└── cli.py          → Interface de linha de comando (entrada/saída via JSON)
```

- **`models.py`**: define os tipos de dados de entrada e saída. Não possui
  lógica de negócio, apenas estrutura.
- **`validator.py`**: contém toda a lógica de negócio, implementada como
  funções puras e testáveis isoladamente (`validar_documento`,
  `calcular_totais`, `validar_campos_obrigatorios`,
  `validar_regras_negocio`, `validar_nota_fiscal`).
- **`cli.py`**: ponto de entrada executável (`python -m nfe_validator.cli
  arquivo.json`), que carrega o JSON, monta os objetos de domínio e imprime
  o resultado da validação.

Nenhum componente adicional (banco de dados, API HTTP, autenticação) foi
adicionado além do que estava especificado — qualquer proposta nesse
sentido permanece registrada como item futuro no board do projeto
("To Do"), não como parte da entrega final.

## 6. Contratos de Erro

Cada erro de validação segue o formato fixo `{ campo, regra, mensagem }`,
onde `regra` é sempre o identificador da regra de negócio (`RN01`–`RN05`)
ou uma categoria estrutural (`campo_obrigatorio`, `campo_invalido`). Este
contrato é estável e não deve ser alterado sem versionamento maior
(SemVer) do pacote.

## 7. Ambiente de Execução (confirmado)

- Python 3.11 (imagem `python:3.11-slim` no Dockerfile)
- Dependências: `pytest`, `pytest-cov` (ver `requirements.txt`)
- Execução via Docker (`docker compose run --rm app pytest -v`) ou local
  (`pip install -r requirements.txt && pytest -v`)

## 8. Divergências entre Spec Inicial e As-Built

| Item | Spec inicial (Entrega 1) | Entrega final (As-Built) | Motivo |
|---|---|---|---|
| RN03 (limite de valor) | Não existia | Adicionada | Identificada como lacuna durante a escrita de testes de borda (Entrega 1, refinamento) |
| Tolerância RN01 | Comparação direta de floats | Comparação com arredondamento explícito a 2 casas decimais | Bug de ponto flutuante identificado na primeira execução real dos testes |
| Cobertura de testes | Não exigida formalmente | 95% de cobertura de código medida e documentada | Exigência formal da Entrega 3 |
| Endpoint HTTP / múltiplas alíquotas | Propostos como itens futuros (board "To Do") | Não implementados nesta versão | Fora do escopo da versão 1.0.0; mantidos como backlog para versões futuras |

Nenhuma outra divergência foi identificada entre o que foi especificado e
o que foi efetivamente entregue no código-fonte da tag `v1.0.0`.
