# Diagrama de Fluxo da Aplicação

Este diagrama descreve o caminho que uma Nota Fiscal percorre desde a
entrada (JSON) até o resultado final de validação, conforme implementado
em `src/nfe_validator/validator.py`.

```
                          ┌───────────────────────────┐
                          │   Entrada: Nota Fiscal    │
                          │   (arquivo JSON / CLI)    │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │ validar_campos_obrigatorios│
                          │ - numero, serie presentes │
                          │ - itens não vazio         │
                          │ - quantidade/valor > 0    │
                          │ - aliquota_icms em [0,1]  │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │      calcular_totais       │
                          │ - valor_calculado (RN01)  │
                          │ - icms_total (RN02)       │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   validar_regras_negocio   │
                          │ - RN01: tolerância R$ 0,01│
                          │ - RN03: limite R$ 100 mil │
                          │ - RN04: data de emissão   │
                          │ - RN05: CPF/CNPJ válido   │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   ResultadoValidacao       │
                          │  { valido, erros[],        │
                          │    valor_calculado,        │
                          │    icms_total }            │
                          └───────────────────────────┘
```

## Descrição textual do fluxo

1. **Entrada**: o usuário fornece um arquivo JSON representando a nota
   fiscal (via CLI: `python -m nfe_validator.cli arquivo.json`).
2. **Validação estrutural**: a função `validar_campos_obrigatorios`
   verifica se todos os campos exigidos pela `SPEC.md` (seção 3) estão
   presentes e com valores minimamente coerentes (não vazios, positivos,
   dentro de faixas).
3. **Cálculo de totais**: independente do resultado da etapa anterior, o
   sistema sempre calcula `valor_calculado` e `icms_total` a partir dos
   itens, pois esses valores são informativos mesmo quando a nota é
   inválida por outro motivo.
4. **Validação de regras de negócio**: com os totais calculados, o
   sistema aplica as regras RN01, RN03, RN04 e RN05 (detalhadas na
   `SPEC.md`, seção 4).
5. **Saída**: um objeto `ResultadoValidacao` consolidado é retornado,
   contendo o veredito final (`valido`), a lista de erros encontrados
   (se houver) e os valores calculados.

Esse fluxo é **stateless** (ADR 003): cada chamada é independente e não
depende de execuções anteriores, o que facilita tanto os testes quanto a
geração de código assistida por IA (cada função pode ser gerada e
validada isoladamente).
