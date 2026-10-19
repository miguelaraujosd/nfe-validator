# Relatório de Cobertura de Código (Coverage)

**Comando executado** (na raiz do projeto):

```
PYTHONPATH=src pytest -v --cov=src/nfe_validator --cov-report=term-missing
```

**Resultado:** 40 testes, 40 aprovados, 0 falhas. **Cobertura total: 99%.**

```
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
src/nfe_validator/__init__.py        0      0   100%
src/nfe_validator/cli.py            21      1    95%   41
src/nfe_validator/models.py         39      0   100%
src/nfe_validator/validator.py      94      0   100%
--------------------------------------------------------------
TOTAL                              154      1    99%
============================== 40 passed in 0.19s ==============================
```

O log completo da execução está em `docs/coverage_output.txt`.

## Evolução da cobertura (registro honesto)

| Medição | Testes | Cobertura | Observação |
|---|---|---|---|
| 1ª medição | 22 | 82% | Com o `cli.py` incluído, a suíte inicial deixava 28 instruções sem cobertura (CLI inteiro, ramos de erro de data, documento e descrição). |
| Medição final | 40 | 99% | Adicionados 18 testes em `tests/test_extra.py` cobrindo cada ramo descoberto. |

Uma medição intermediária de 95% chegou a ser relatada informalmente, mas foi
feita sobre uma cópia do projeto sem o `cli.py`, portanto não representava o
código entregue. O número válido é o da tabela acima.

## Linha não coberta

- `cli.py`, linha 41: a chamada `main()` dentro do bloco
  `if __name__ == "__main__":`. Essa linha só executa quando o módulo é rodado
  como script (`python -m nfe_validator.cli`); os testes chamam `main()`
  diretamente, e o fluxo de ponta a ponta foi exercitado manualmente nos
  exemplos da pasta `exemplos/`.

## Cobertura por regra de negócio

Todas as regras (RN01 a RN05), a validação de campos obrigatórios e a
serialização do resultado (`to_dict`) estão com 100% das linhas exercitadas
por testes automatizados.
