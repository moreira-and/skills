# Modelo de Conteúdo e Rastreabilidade

O resultado não introduz dados persistidos em runtime. Este modelo descreve entidades documentais usadas para organizar a migração e verificar cobertura.

## Entidades

### Fonte legada

- **Identidade**: caminho relativo único sob `legado/`.
- **Tipo**: orientação principal, referência, metadata de consumidor ou ferramenta executável.
- **Conteúdo útil**: regras, decisões, exemplos, gates, avisos ou comportamento automatizado identificados na leitura.
- **Destino**: skill, referência, script, consolidação de duplicata ou não incorporação justificada.
- **Proveniência**: caminho original mantido no mapa de conteúdo; os arquivos de `legado/` permanecem inalterados.

### Skill

- **Identidade**: diretório de nome único no catálogo `skills/` e seu `SKILL.md`.
- **Capacidade**: uma responsabilidade principal que pode ser ativada e usada sem carregar outra skill.
- **Fronteira**: solicitações atendidas, solicitações não atendidas e critérios para referências complementares.
- **Instruções essenciais**: fluxo curto, obrigatório versus recomendação, limites e riscos.
- **Referências**: detalhes focados vinculados por links Markdown relativos, sem mais de um diretório de profundidade.
- **Validação**: contrato estrutural local mais revisão semântica.

### Regra de negócio

- **Identidade**: identificador no mapa de fontes durante a migração.
- **Semântica**: decisão de negócio ou convenção organizacional, sem ser generalizada como padrão de mercado quando não for.
- **Fonte autorizada**: caminho legado que contém a formulação mais precisa ou a regra escolhida para resolver conflito.
- **Local canônico**: uma referência ou instrução essencial no catálogo.
- **Validação**: como o revisor demonstra que a regra foi preservada e não contradiz outra regra canônica.

### Ferramenta executável

- **Identidade**: caminho dentro de `skills/<skill>/scripts/`.
- **Propósito**: verificação local limitada e expressa claramente.
- **Uso e dependências**: seção correspondente em `scripts/README.md`, incluindo `Usage:` e `Dependencies:`.
- **Saída**: achados e código de saída previsíveis; erros de entrada devem ser explícitos.
- **Limite**: parser heurístico não é confirmação de sintaxe do runtime ou de deploy.

## Relações e regras de integridade

- Cada fonte legada tem exatamente uma decisão de destino rastreável, embora seu conteúdo possa mapear para várias referências somente quando regras distintas realmente pertencem a responsabilidades diferentes.
- Cada regra de negócio considerada útil tem uma localização canônica identificável e uma fonte de origem.
- Cada skill tem uma capacidade principal; uma referência cruzada pode ser complementar, nunca pré-requisito oculto para entender a skill de origem.
- Cada script publicado tem documentação e casos de teste para seu contrato observável.
- Duplicatas são registradas como consolidadas, sem replicar regras; diferenças de conteúdo não são tratadas como duplicatas sem comparação.
- Configurações de consumidor e exemplos Databricks dependentes de versão são marcados como tais; ausência de fonte verificável impede certificação de compatibilidade.