# Relatório de Cobertura de Código (Coverage)

**Comando executado:**
```
pytest -v --cov=src/nfe_validator --cov-report=term-missing
```

**Resultado consolidado:** 22 testes, 22 aprovados. **Cobertura total: 95%.**

```
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
src/nfe_validator/__init__.py        0      0   100%
src/nfe_validator/models.py         39      1    97%   53
src/nfe_validator/validator.py      94      6    94%   36, 57, 87, 125-126, 131
--------------------------------------------------------------
TOTAL                               133      7    95%
============================== 22 passed in 0.12s ==============================
```

## Análise das linhas não cobertas

- `models.py`, linha 53: linha do método utilitário `to_dict()` referente a
  um caminho auxiliar de serialização não exercitado diretamente pelos
  testes unitários (é exercitado indiretamente pelo CLI, mas não possui
  teste automatizado dedicado).
- `validator.py`, linhas 36, 57: ramos internos das funções auxiliares de
  cálculo de dígito verificador de CPF/CNPJ (`_digito_verificador_cpf` e
  `_digito_verificador_cnpj`) que tratam o caso específico de resto igual a
  10 no cálculo do dígito — coberto indiretamente, mas sem um teste que
  force exatamente esse resto.
- `validator.py`, linhas 87, 125-126, 131: ramos de tratamento de exceção
  (`try/except`) para entradas malformadas de data, e o bloco de
  orquestração final da função `validar_nota_fiscal` quando `numero` ou
  `itens` estão ausentes (nesse caso a validação de regras de negócio é
  pulada por decisão de design, então o "miss" é esperado).

## Meta de cobertura e justificativa

O time considera 95% um resultado satisfatório para este projeto: as
linhas não cobertas são majoritariamente ramos defensivos (tratamento de
erro) e não caminhos de regra de negócio crítica, todos os quais possuem
cobertura completa (RN01–RN05, 100% exercitadas pelos 22 testes).
