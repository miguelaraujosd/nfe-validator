# Roteiro do Vídeo de Demonstração (3–5 minutos)

Como gravar (sem precisar de nenhum programa pago):
- **Windows:** tecla `Windows + G` abre a Game Bar → botão de gravar tela.
- Ou instale o **OBS Studio** (gratuito) ou use o **Loom** (gratuito, já sobe
  pra nuvem e gera o link direto — mais rápido pra essa entrega).

Depois de gravar, suba no YouTube (pode ser "não listado"), Google Drive
(com link de acesso liberado) ou Loom, e copie o link pro PDF final.

---

## Roteiro (siga na ordem, cronometrando)

**[0:00 – 0:30] Introdução**
> "Oi, somos o grupo [nome do grupo]. Esse é o NFe Validator, um sistema
> que valida notas fiscais em JSON contra regras de negócio de impostos,
> campos obrigatórios e limites de valor. Ele foi desenvolvido usando o
> fluxo Spec-Driven Development com apoio do Claude Code."

**[0:30 – 1:15] Mostrar a especificação (SPEC.md)**
- Abra o `SPEC.md` no GitHub, role rapidamente mostrando as regras de
  negócio (RN01 a RN05).
> "Antes de qualquer código, escrevemos essa especificação com as regras
> de negócio e os contratos de entrada e saída."

**[1:15 – 2:30] Demonstração funcional (a parte mais importante)**
- Abra o terminal, rode:
  ```
  python -m nfe_validator.cli exemplos/nota_valida.json
  ```
  mostre o resultado `"valido": true`.
- Depois rode com um exemplo inválido:
  ```
  python -m nfe_validator.cli exemplos/nota_cpf_invalido.json
  ```
  mostre o erro retornado (`"valido": false`, com o campo e a regra
  violada).
> "Aqui vemos a aplicação validando uma nota correta, e depois rejeitando
> uma nota com CPF inválido, mostrando exatamente qual regra foi violada."

**[2:30 – 3:30] Rodar a suíte de testes ao vivo**
- No terminal, rode:
  ```
  pytest -v --cov=src/nfe_validator --cov-report=term-missing
  ```
- Deixe rodar até o final, mostrando `22 passed` e a cobertura de 95%.
> "Nossa suíte tem 22 testes automatizados cobrindo casos normais e de
> borda, com 100% de aprovação e 95% de cobertura de código."

**[3:30 – 4:15] Mostrar o repositório e a release**
- Mostre a página do GitHub, a aba "Releases" com a tag `v1.0.0`.
> "O projeto está versionado no GitHub com a release oficial v1.0.0,
> seguindo um fluxo de branches protegidas e Pull Requests revisados."

**[4:15 – 5:00] Encerramento / retrospectiva**
> "Como principal aprendizado, vimos que usar um agente de IA dentro de um
> fluxo com especificação clara e testes automatizados torna o
> desenvolvimento mais rápido sem abrir mão de controle e revisão humana.
> Obrigado!"

---

**Dica:** não precisa decorar o texto, só ter esse roteiro aberto numa
aba e ir seguindo enquanto grava a tela.
