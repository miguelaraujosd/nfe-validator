# Análise Comparativa e Avaliação Crítica de IA

## 1. Análise Comparativa de Ferramentas

O grupo utilizou o **Claude Code** como agente principal de geração e
auxílio de código ao longo de todo o fluxo SDD deste projeto. Abaixo, uma
comparação com outras ferramentas do mesmo ecossistema, baseada em
características documentadas publicamente e na experiência de uso direto
com Claude Code neste projeto.

| Critério | Claude Code | Codex CLI | Cursor | Antigravity |
|---|---|---|---|---|
| **Modelo de interação** | Agente de terminal, orientado a tarefas longas, com acesso a arquivos, shell e ferramentas externas | Agente de terminal similar, focado em geração e edição via linha de comando | IDE completo com agente integrado ao editor (inline + chat) | Agente orientado a fluxo multi-etapas com foco em automação de tarefas |
| **Fidelidade a especificação (SDD)** | Alta — segue instruções de contexto (`.claude/CLAUDE.md`) de forma consistente ao longo de sessões longas | Boa, mas orientado mais à tarefa pontual do que ao contexto de projeto completo | Boa dentro do editor, mas o contexto de projeto pode se perder em edições muito longas | Variável — mais forte em automação de múltiplos passos do que em aderência estrita a uma spec fixa |
| **Qualidade do código gerado** | Boa, com tendência a seguir padrões definidos explicitamente (tipagem, docstrings, nomeação) | Boa, historicamente forte em tarefas de codificação pura | Boa, com vantagem de refatoração assistida por causa da integração com o editor | Boa para tarefas de automação; qualidade de código "puro" pode variar mais |
| **Rastreabilidade das decisões** | Alta — quando orientado a documentar (ADRs, mensagens de commit, comentários citando regras de negócio) | Média — depende fortemente do prompt do usuário a cada chamada | Média-alta, pois o histórico de chat fica dentro do IDE | Média — foco maior em execução do que em documentação da decisão |
| **Curva de aprendizado da equipe** | Baixa a média — requer entender o fluxo de terminal, mas a documentação de contexto é simples (arquivos Markdown) | Baixa a média, similar ao Claude Code | Baixa — familiar para quem já usa um IDE | Média — conceito de "agente multi-etapas" é menos intuitivo para iniciantes |
| **Impacto observado na qualidade da spec** | Positivo: forçar o agente a seguir a `SPEC.md` obrigou o time a escrever regras de negócio mais precisas antes de codar | Depende do disciplinamento do usuário em manter uma spec separada | Depende, pois o IDE facilita "pular direto pro código" | Pode reforçar disciplina de processo se usado com checklists explícitos |

**Conclusão da comparação:** para um fluxo estritamente SDD, ferramentas de
agente de terminal orientadas a arquivos de contexto persistentes (como
o Claude Code) tendem a manter maior fidelidade à especificação ao longo
de uma sessão de trabalho longa, pois o contexto do projeto (regras de
negócio, convenções) é lido explicitamente antes de cada tarefa. IDEs
com agente integrado (Cursor) favorecem iteração rápida, mas exigem mais
disciplina do time para não pular a etapa de especificação.

## 2. Ética, Limites e Segurança do Uso de IA

### 2.1. Riscos de alucinação de código e geração de código inseguro ou destrutivo

Durante o desenvolvimento, o agente de IA gerou código sintaticamente
correto em praticamente todos os casos, mas isso não elimina o risco de
**alucinação lógica**: código que roda sem erros, mas implementa uma
regra de negócio ligeiramente diferente da pretendida. Um exemplo real
encontrado neste projeto foi o bug de arredondamento de ponto flutuante
na comparação de valores (RN01) — o código gerado inicialmente "parecia"
correto e só falhou ao ser exercitado por um teste de borda específico.
Isso reforça que:

- Código gerado por IA deve ser tratado como uma **proposta a ser
  verificada**, nunca como verdade definitiva, especialmente em regras
  de negócio numéricas ou financeiras.
- Testes automatizados cobrindo casos de borda são a principal defesa
  contra esse tipo de erro sutil, e não podem ser delegados
  integralmente à IA sem revisão humana dos casos escolhidos.
- Em contextos de maior risco (ex: manipulação de arquivos, comandos de
  shell, exclusão de dados), qualquer sugestão do agente que envolva
  ações destrutivas (delete, force-push, sobrescrita de arquivos) deve
  ser explicitamente aprovada por um humano antes da execução — o que
  este projeto seguiu ao tratar cada `git push --force` como uma decisão
  humana explícita, não automatizada.

### 2.2. Vazamento de dados, privacidade e riscos de confidencialidade ao expor contexto aos modelos

Ao usar um agente de IA operando sobre o repositório do projeto, todo o
conteúdo de arquivos lidos pelo agente (código, specs, dados de exemplo)
passa por um provedor externo de modelo de linguagem. Isso implica
riscos reais quando o projeto envolve dados sensíveis:

- Nunca incluir dados reais de clientes, CPFs/CNPJs verdadeiros, chaves
  de API ou credenciais em arquivos versionados ou usados como contexto
  para o agente — neste projeto, todos os exemplos de nota fiscal usam
  dados fictícios (CNPJs e CPFs matematicamente válidos, mas não
  associados a empresas ou pessoas reais).
- Arquivos de configuração sensíveis (`.env`, chaves de acesso, tokens)
  devem estar no `.gitignore` e nunca devem ser lidos ou colados como
  contexto para o agente de IA.
- Em ambientes corporativos reais, é necessário verificar a política de
  retenção de dados do provedor de IA utilizado (se o conteúdo enviado é
  usado para treinar modelos futuros, por quanto tempo é retido, etc.)
  antes de expor qualquer informação proprietária ou regulada (ex: dados
  fiscais reais, protegidos por sigilo).

### 2.3. Propriedade Intelectual (IP) e direitos autorais do código gerado por IA

A questão de quem detém os direitos sobre código gerado por um agente de
IA ainda é uma área juridicamente não totalmente pacificada, e o time
adotou uma postura conservadora:

- O código gerado com auxílio do Claude Code neste projeto foi sempre
  revisado, ajustado e testado por membros humanos do time antes de ser
  incorporado ao repositório — a autoria intelectual e a responsabilidade
  final pelo código permanecem com os desenvolvedores humanos, que
  validaram e assumiram cada trecho.
- Especificações e regras de negócio (a parte mais "proprietária" do
  projeto, do ponto de vista de propriedade intelectual) foram escritas
  pelo time antes de qualquer geração de código, o que preserva a autoria
  humana sobre a concepção da solução.
- Este é um projeto acadêmico com fins didáticos e sem dados ou modelos
  de negócio proprietários reais, o que reduz o risco prático de disputa
  de IP; mesmo assim, o time optou por documentar claramente (neste
  relatório e no README) o uso de IA como ferramenta de apoio, seguindo
  boas práticas de transparência.

### 2.4. A centralidade e obrigatoriedade da homologação e revisão humana no fluxo SDD

O uso de um fluxo Spec-Driven Development reforça, e não substitui, a
necessidade de revisão humana:

- A especificação (`SPEC.md`) funciona como um contrato entre a intenção
  do time e o código gerado, mas **a IA não valida sozinha se o código
  atende à especificação** — essa validação é feita por meio de testes
  escritos e revisados por humanos, e por revisão manual do código antes
  do merge (Pull Requests).
- Neste projeto, toda mudança de código passou pelo fluxo de branch
  protegida (`main`) + Pull Request, garantindo que nenhuma alteração
  fosse incorporada sem, no mínimo, uma etapa de revisão e execução da
  suíte de testes automatizados.
- A homologação humana é particularmente crítica em dois momentos: (1)
  ao aceitar uma regra de negócio interpretada pela IA a partir de uma
  especificação ambígua — a interpretação precisa ser confirmada pelo
  time antes de virar código definitivo; e (2) ao aceitar testes gerados
  automaticamente — um teste mal escrito pode "passar" sem realmente
  validar a regra de negócio pretendida, dando uma falsa sensação de
  segurança.
- Conclusão do time: um fluxo SDD assistido por IA acelera a produção de
  código e testes, mas desloca o trabalho humano da escrita linha a
  linha para a **verificação e julgamento** — exigindo, portanto, tanto
  ou mais rigor de revisão do que o desenvolvimento tradicional.
