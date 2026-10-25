# Checklist de Validação e Manifesto de Migração

Use esta referência para verificar que artefatos produzidos preservam comportamento e podem ser revisados. Um linter não substitui revisão semântica nem validação de deploy.

## Verificações automatizadas

- Executar o validador estático de pipeline disponível; corrigir `ERROR` e avaliar cada `WARNING`.
- Executar o validador de skills para metadados, nomes, links e documentação de scripts.
- Quando disponível, executar validação de bundle no target correto.
- Registrar a versão e o ambiente dos comandos; deixar claro se a validação real de deploy não foi executada.

## Verificações manuais

### Nomes e referências

- Nenhum nome legado permanece no código novo, salvo identificação de origem em comentários de rastreabilidade.
- Nomes seguem a convenção de projeto fornecida, se houver; nenhum schema ou namespace legado permanece sem justificativa.
- Os identificadores de catálogo, schema, tabela e coluna usam o substantivo principal no singular; campos técnicos fixos da plataforma e nomes de diretórios permanecem conforme suas APIs.
- Cada referência de origem existe como objeto do projeto ou é uma fonte externa documentada com pendência explícita.
- Objetos consumidos como stream correspondem a definições compatíveis; não há dependências circulares.

### Dados estáticos

- Contagem das linhas/tuplas `VALUES` corresponde aos elementos originais.
- Ordem das colunas e valores `NULL`, `TRUE`, `FALSE` foram preservados.
- Apóstrofos foram escapados e tipos estão declarados.

### Lógica e semântica

- Cada regra de negócio identificada no inventário tem destino rastreável.
- Comentários de catálogo, schema, tabela e coluna descrevem o domínio, granularidade, significado, unidades e tratamento de nulos necessários para interpretar os dados; não dependem de conhecimento privado não registrado.
- Não houve regra omitida nem mudança semântica sem justificativa e aprovação registrada.
- Mudanças de tipo, filtro, join, deduplicação, ordenação, timezone, nulidade ou reprocessamento foram tratadas como potenciais mudanças de comportamento.
- Bloqueios e decisões pendentes estão claros; não há placeholder de produção.

### Bundle e execução

- Recursos, bibliotecas e caminhos do bundle estão alinhados com a estrutura gerada.
- Dependências do job refletem o grafo aprovado.
- Variáveis e targets foram conferidos no ambiente; conteúdo sensível não foi gravado em texto plano.
- A declaração de pipeline não foi apresentada como execução avulsa quando exige recurso registrado.

## Manifesto de entrega

O manifesto final deve registrar:

- origem e data da migração;
- contagem de scripts lidos e artefatos gerados por tipo;
- mapa de nomes legado→canônico com justificativas;
- regras de negócio preservadas e localização no objeto de destino;
- decisões de migração, impacto e aprovador;
- bloqueios resolvidos e pendências restantes;
- resultado dos validadores, avisos aceitos com justificativa e versão/ambiente das verificações.

## Critério de conclusão

Considerar a entrega pronta quando não houver erro automatizado sem resolução, referências inconsistentes, placeholder em produção ou regra de negócio sem destino; toda mudança semântica tem aprovação; e as pendências restantes são explicitamente classificadas. Uma verificação de bundle/deploy indisponível deve ser identificada como não executada, não como aprovada.