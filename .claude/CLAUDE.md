# Instruções para o Agente de IA (Claude Code) — Projeto NFe Validator

## Papel do agente neste projeto

Você está atuando dentro de um fluxo **Spec-Driven Development (SDD)**. A
fonte única da verdade sobre o comportamento esperado do sistema é o arquivo
`SPEC.md` na raiz do repositório. Nunca invente regras de negócio que não
estejam lá — se algo parecer ambíguo ou faltando, sinalize isso explicitamente
como um gap de especificação em vez de assumir um comportamento.

## Ordem de trabalho obrigatória

1. Leia `SPEC.md` por completo antes de gerar ou alterar qualquer código.
2. Ao implementar uma regra de negócio (RN01, RN02, ...), cite no comentário
   do código qual regra está sendo implementada.
3. Para cada regra de negócio implementada, gere também os casos de teste
   correspondentes na seção "Casos de Borda" da SPEC.md.
4. Se, ao escrever testes, você perceber um caso não coberto pela spec,
   pare e proponha uma atualização em `SPEC.md` (seção 7 — Histórico de
   Refinamento) antes de codar a solução para esse caso.
5. Nunca implemente integração real com SEFAZ, autenticação, ou banco de
   dados — está fora do escopo definido em `SPEC.md`, seção 2.

## Padrões de código

- Python 3.11, tipagem estática com `dataclasses` e type hints em todas as
  funções públicas.
- Funções de validação devem ser puras (sem efeitos colaterais, sem I/O).
- Nomes de função em português quando representam conceitos de negócio
  (ex: `validar_documento`), em inglês quando são utilitários genéricos.
- Toda função pública deve ter docstring citando a(s) regra(s) de negócio
  (RNxx) que implementa.

## Padrões de teste

- Framework: `pytest`.
- Use `@pytest.mark.parametrize` para cobrir múltiplos edge cases de uma
  mesma regra sem duplicar a estrutura do teste.
- Nomeie os testes como `test_<regra>_<cenario>`, ex:
  `test_rn03_valor_acima_limite_sem_autorizacao_falha`.
- Todo teste deve referenciar, em comentário, o item da seção 6 (Casos de
  Borda) da SPEC.md que ele cobre.

## O que NÃO fazer

- Não adicionar dependências externas além das já listadas em
  `requirements.txt` sem justificar em um novo ADR.
- Não remover ou "simplificar" regras de negócio da SPEC.md ao gerar código
  — se uma regra parecer errada, isso é uma discussão de spec, não uma
  decisão de implementação.
- Não gerar código de infraestrutura (Docker, CI) sem que isso esteja
  pedido explicitamente na tarefa/issue atual.
