# Relatório de Execução da Suíte de Testes

**Comando executado:** `pytest -v` (ambiente Python 3.12 / pytest 9.1.1)
**Resultado:** 22 testes, 22 passaram, 0 falharam.

## Log de execução

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /app
collecting ... collected 22 items

tests/test_validator.py::test_nota_valida_passa_sem_erros PASSED         [  4%]
tests/test_validator.py::test_edge_1_nota_sem_itens_invalida PASSED      [  9%]
tests/test_validator.py::test_edge_2_item_com_quantidade_ou_valor_invalido[-1-50.0] PASSED [ 13%]
tests/test_validator.py::test_edge_2_item_com_quantidade_ou_valor_invalido[0-50.0] PASSED [ 18%]
tests/test_validator.py::test_edge_2_item_com_quantidade_ou_valor_invalido[2-0] PASSED [ 22%]
tests/test_validator.py::test_edge_2_item_com_quantidade_ou_valor_invalido[2--10] PASSED [ 27%]
tests/test_validator.py::test_edge_3_aliquota_icms_fora_do_intervalo[1.5] PASSED [ 31%]
tests/test_validator.py::test_edge_3_aliquota_icms_fora_do_intervalo[-0.1] PASSED [ 36%]
tests/test_validator.py::test_edge_4_diferenca_de_um_centavo_passa PASSED [ 40%]
tests/test_validator.py::test_edge_4_diferenca_de_dois_centavos_falha PASSED [ 45%]
tests/test_validator.py::test_edge_5_documento_com_digitos_repetidos_invalido[11111111111] PASSED [ 50%]
tests/test_validator.py::test_edge_5_documento_com_digitos_repetidos_invalido[11111111000111] PASSED [ 54%]
tests/test_validator.py::test_documento_valido_cpf_e_cnpj PASSED         [ 59%]
tests/test_validator.py::test_edge_6_data_emissao_futura_invalida PASSED [ 63%]
tests/test_validator.py::test_edge_7_data_emissao_vencida_invalida PASSED [ 68%]
tests/test_validator.py::test_edge_8_valor_exatamente_no_limite_nao_exige_autorizacao PASSED [ 72%]
tests/test_validator.py::test_edge_9_valor_acima_do_limite_sem_autorizacao_falha PASSED [ 77%]
tests/test_validator.py::test_edge_9_valor_acima_do_limite_com_autorizacao_passa_rn03 PASSED [ 81%]
tests/test_validator.py::test_edge_10_campo_obrigatorio_ausente[numero-] PASSED [ 86%]
tests/test_validator.py::test_edge_10_campo_obrigatorio_ausente[serie-] PASSED [ 90%]
tests/test_validator.py::test_edge_10_razao_social_emitente_ausente PASSED [ 95%]
tests/test_validator.py::test_edge_10_nome_destinatario_ausente PASSED   [100%]

============================== 22 passed in 0.04s ===============================
```

## Bug encontrado e corrigido durante a execução (evidência de refinamento)

Na primeira execução da suíte, o teste `test_edge_4_diferenca_de_um_centavo_passa`
falhou com `AssertionError`. A causa raiz foi erro de representação de ponto
flutuante em Python (`100.01 - 100.00` não resulta exatamente em `0.01`).

**Correção aplicada em `validator.py` (RN01):** a diferença entre valor
declarado e valor calculado passou a ser arredondada para 2 casas decimais
antes da comparação com a tolerância:

```python
diferenca = round(abs(nota.valor_total_declarado - valor_calculado), 2)
if diferenca > TOLERANCIA_CENTAVOS:
    ...
```

Após a correção, os 22 testes passaram. Esse episódio está registrado como
exemplo real de "Refinamento por Feedback de Testes" (ver `SPEC.md`, seção 7).

> Para reproduzir este relatório no ambiente padronizado:
> `docker compose run --rm app pytest -v`
> Anexe aqui (ou no PDF de submissão) o print do terminal com esse resultado.
