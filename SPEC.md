# SPEC.md — Especificação Técnica: Validador/Parser de Notas Fiscais

Versão: 1.1
Status: Em refinamento (ver seção 7 — Histórico de Alterações)

## 1. Problema

Empresas que emitem notas fiscais eletrônicas precisam garantir, antes de
qualquer envio ou processamento posterior, que os dados básicos da nota
(emitente, destinatário, itens, impostos) estejam corretos e coerentes. Este
projeto implementa um **validador/parser** que recebe uma Nota Fiscal em
formato JSON e retorna:

- `valido: true` se todos os campos e regras passarem, ou
- `valido: false` com uma lista detalhada de erros encontrados.

## 2. Escopo

**Dentro do escopo:**
- Validação estrutural (campos obrigatórios presentes e com tipo correto).
- Validação de regras de negócio simplificadas (impostos, limites de valor).
- Cálculo e conferência do valor total da nota a partir dos itens.

**Fora do escopo:**
- Integração real com SEFAZ / assinatura digital / XML oficial da NF-e.
- Persistência em banco de dados (o serviço é stateless).
- Autenticação de usuários.

## 3. Contrato de Entrada (Input)

Formato: JSON. Exemplo:

```json
{
  "numero": "000123",
  "serie": "1",
  "data_emissao": "2026-09-10",
  "emitente": {
    "cnpj": "12345678000199",
    "razao_social": "Empresa Exemplo LTDA"
  },
  "destinatario": {
    "documento": "12345678900",
    "nome": "Cliente Exemplo"
  },
  "itens": [
    {
      "descricao": "Produto A",
      "quantidade": 2,
      "valor_unitario": 50.00,
      "aliquota_icms": 0.18
    }
  ],
  "valor_total_declarado": 118.00
}
```

### Campos obrigatórios

| Campo | Tipo | Obrigatório | Regra |
|---|---|---|---|
| `numero` | string | Sim | Não vazio, até 9 dígitos |
| `serie` | string | Sim | Não vazio |
| `data_emissao` | string (ISO 8601) | Sim | Data válida, não pode ser futura |
| `emitente.cnpj` | string | Sim | 14 dígitos numéricos, dígito verificador válido |
| `emitente.razao_social` | string | Sim | Não vazio |
| `destinatario.documento` | string | Sim | CPF (11 dígitos) ou CNPJ (14 dígitos) válido |
| `destinatario.nome` | string | Sim | Não vazio |
| `itens` | lista | Sim | Ao menos 1 item |
| `itens[].descricao` | string | Sim | Não vazio |
| `itens[].quantidade` | number | Sim | > 0 |
| `itens[].valor_unitario` | number | Sim | > 0 |
| `itens[].aliquota_icms` | number | Sim | Entre 0 e 1 (0% a 100%) |
| `valor_total_declarado` | number | Sim | > 0 |

## 4. Regras de Negócio

**RN01 — Cálculo do valor total.**
`valor_calculado = soma(quantidade * valor_unitario)` para todos os itens.
`valor_total_declarado` deve ser igual a `valor_calculado` com tolerância de
R$ 0,01 (arredondamento).

**RN02 — Cálculo de ICMS por item.**
`icms_item = quantidade * valor_unitario * aliquota_icms`.
O total de ICMS da nota é a soma do ICMS de todos os itens e deve ser
retornado no resultado da validação (campo informativo, não bloqueante).

**RN03 — Limite de valor por nota (regra fiscal simplificada).**
Notas com `valor_total_declarado > 100.000,00` exigem o campo opcional
`autorizacao_especial: true`. Se ausente ou `false`, a nota é inválida.

**RN04 — Data de emissão.**
`data_emissao` não pode ser superior à data atual do sistema, nem anterior a
5 anos da data atual (nota "vencida" para fins deste sistema).

**RN05 — Documento do destinatário.**
Deve ser um CPF (11 dígitos) ou CNPJ (14 dígitos) numericamente válido,
segundo o algoritmo de dígito verificador padrão de cada um.

## 5. Contrato de Saída (Output)

```json
{
  "valido": false,
  "erros": [
    {
      "campo": "valor_total_declarado",
      "regra": "RN01",
      "mensagem": "Valor declarado (118.00) difere do valor calculado (100.00)."
    }
  ],
  "valor_calculado": 100.00,
  "icms_total": 18.00
}
```

- `valido`: boolean.
- `erros`: lista (vazia se `valido = true`), cada erro referencia o campo, a
  regra violada (ID da regra de negócio) e uma mensagem legível.
- `valor_calculado` e `icms_total`: sempre retornados quando os itens puderem
  ser processados, mesmo que a nota seja inválida por outro motivo.

## 6. Casos de Borda (Edge Cases) — cobertura obrigatória nos testes

1. Nota sem nenhum item (`itens: []`).
2. Item com `quantidade` ou `valor_unitario` negativo ou igual a zero.
3. `aliquota_icms` fora do intervalo [0, 1] (ex: 1.5 ou -0.1).
4. `valor_total_declarado` com diferença de arredondamento de exatamente
   R$ 0,01 (deve passar) vs R$ 0,02 (deve falhar).
5. CNPJ/CPF com todos os dígitos iguais (ex: "111.111.111-11") — inválido
   pelo algoritmo padrão mesmo tendo o número certo de dígitos.
6. `data_emissao` no futuro.
7. `data_emissao` há mais de 5 anos.
8. Nota com valor exatamente igual a R$ 100.000,00 (limite, não deve exigir
   autorização especial — regra é "maior que", não "maior ou igual").
9. Nota com valor de R$ 100.000,01 sem `autorizacao_especial`.
10. Campos obrigatórios ausentes (um teste por campo crítico).
11. JSON malformado / tipos incorretos (ex: `quantidade` como string).

## 7. Histórico de Refinamento da Especificação

| Data | Alteração | Motivo |
|---|---|---|
| v1.0 | Versão inicial com RN01, RN02, RN04, RN05 | Primeira decomposição do problema |
| v1.1 | Adicionada RN03 (limite de R$ 100.000) e edge cases 8 e 9 | Durante a escrita dos testes, percebemos que não havia regra alguma tratando notas de valor muito alto — gap identificado por revisão do grupo |
| v1.1 | Definida tolerância de R$ 0,01 na RN01 | Testes iniciais falhavam por erro de ponto flutuante ao comparar valores decimais exatos |

> Este documento deve ser atualizado a cada rodada de revisão/teste que
> revele ambiguidade ou lacuna na especificação original.

## 8. Decomposição em Unidades (para desenvolvimento iterativo)

| Unidade | Responsabilidade | Testável isoladamente? |
|---|---|---|
| `models.py` | Estruturas de dados (dataclasses) da Nota, Item, Emitente, Destinatário | Sim (construção de objetos) |
| `validator.py::validar_campos_obrigatorios` | Checagem estrutural | Sim |
| `validator.py::validar_documento` | Algoritmo de CPF/CNPJ | Sim |
| `validator.py::calcular_totais` | RN01 e RN02 | Sim |
| `validator.py::validar_regras_negocio` | RN03, RN04 | Sim |
| `validator.py::validar_nota_fiscal` | Orquestra as demais unidades | Sim (teste de integração) |
