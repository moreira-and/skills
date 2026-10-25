# Nomenclatura de Tabelas e Views

Use nomes que descrevam o conteúdo, sigam a convenção do catálogo e sejam fáceis de interpretar. Nesta skill, os identificadores de catálogo, schema e tabela usam substantivo principal no singular. Essa é uma decisão explícita de naming deste catálogo; outras convenções podem existir no mercado.

## Regra

- Preferir nomes concisos e semânticos, em um único padrão de caixa e separação escolhido para o catálogo.
- Usar o substantivo principal no singular em catálogo, schema e tabela. Uma tabela representa um tipo de entidade; conter várias linhas não exige pluralizar o nome.
- Identificar o conteúdo sem repetir detalhes já expressos pelo caminho, catálogo, schema ou definição.
- Incluir a origem no nome somente quando distinguir fontes agrega informação útil; não codificar fornecedor, cliente ou unidade de negócio sem necessidade.
- Para objetos derivados, nomear o resultado ou propósito; não codificar estágio físico ou tipo de objeto se esses detalhes já estiverem disponíveis em outro lugar.

## Proibido

- Evitar nomes vagos, temporários ou dependentes do autor, como `table1`, `tmp` e `final_result`.
- Evitar prefixos redundantes que apenas repetem o tipo de objeto ou a camada, exceto quando uma convenção organizacional explícita os exigir.

## Revisão

1. Confirmar que o nome segue a convenção escolhida e que o núcleo nominal está no singular.
2. Confirmar que o conceito é compreensível e não é redundante.
3. Verificar se origem, camada ou tipo precisam realmente fazer parte do identificador.

Se não houver padrão fornecido, apresentar a proposta como recomendação. Se faltar contexto semântico, pedir esclarecimento em vez de inventar o significado.

**Exemplos neutros**: `sample_catalog.sample_schema.event_record`, `source_record`, `daily_metric`; `sample_catalog`, `sample_schema` e os substantivos centrais estão no singular. Nomes como `events`, `records` e `metrics` pluralizam o núcleo e devem ser evitados nesta convenção. `table1`, `tmp` e `final_result` não comunicam propósito.