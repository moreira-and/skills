# Pesquisa: Agente de migração Databricks

## D1 - O "agente" é uma skill

- **Decisão**: entregar como skill Agent Skills em `skills/databricks-migration-engineer/`.
- **Justificativa**: a documentação do Genie Code ([Extend Genie Code with agent skills](https://docs.databricks.com/aws/en/genie-code/skills)) descreve skills no padrão agentskills.io, carregadas automaticamente pela descrição ou por `@`, em `Workspace/.assistant/skills/` (workspace) ou `/Users/{usuario}/.assistant/skills/` (usuário). Não há formato de agente separado. A constituição exige o padrão aberto.
- **Alternativas**: arquivo `.agent.md` do Copilot (não é consumido pelo Genie Code); instruções customizadas do Genie Code (globais, sempre aplicadas, sem carga sob demanda, o que contraria o uso em massa com contexto eficiente).

## D2 - Delegar regras às skills irmãs

- **Decisão**: referenciar pelo nome da skill (não por link `../`, que o validador do catálogo rejeita) e não copiar conteúdo.
- **Justificativa**: evita deriva e contradição (FR-002, SC-002); o Genie Code carrega skills por descrição ou `@`, então a referência por nome funciona com as skills lado a lado no workspace.
- **Alternativas**: consolidar tudo numa skill grande (viola responsabilidade única e gasta contexto).

## D3 - Conteúdo da skill

- **Decisão**: `SKILL.md` curto, com persona, escopo, quando não usar, fluxo e limites. Detalhes em `references/` carregados sob demanda.
- **Justificativa**: divulgação progressiva, como pede o padrão e a constituição.

## D4 - Segurança no Genie Code

- **Decisão**: o texto da skill proíbe deploy, commit/push e produção. Ações no workspace de teste ficam restritas a leitura e validação, e as destrutivas exigem confirmação.
- **Justificativa**: o padrão não impõe permissões; a restrição é instrução, não controle técnico. O README deve dizer que as permissões reais dependem do workspace e do Genie Code.
- **Alternativas**: `allowed-tools` (experimental e sem suporte confirmado no consumidor, então não é usado).

## D5 - Idioma e versões

- **Decisão**: português, como as skills irmãs. Compatibilidade de sintaxe e versão não confirmada é marcada como "não validada".

Nenhum ponto `NEEDS CLARIFICATION` restante.
