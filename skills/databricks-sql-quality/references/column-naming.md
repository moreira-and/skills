# Nomenclatura de Colunas

Use nomes de coluna que descrevam o significado e sejam consistentes com o catálogo. Nesta skill, o substantivo principal de cada coluna fica no singular, inclusive quando o valor representa uma coleção. Prefixos são opcionais e dependem de uma convenção explicitamente adotada.

## Formato e prefixos

`snake_case` é uma opção comum em SQL, mas o formato deve ser consistente com o catálogo e ferramentas existentes. Um prefixo pode indicar papel semântico se o projeto o adotar; não repetir nele o tipo físico ou o significado do restante do nome. Manter o substantivo principal no singular: `item_count`, não `items_count`; `address_list`, não `addresses`.

| Papel | Nome descritivo | Prefixo opcional em alguns catálogos |
|---|---|---|
| Identificador | `record_id` | `id_record` |
| Referência | `source_record_id` | `fk_source_record` |
| Timestamp | `created_at` | `dh_created_at` |
| Medida | `total_amount` | `amount_total` ou um prefixo local consistente |
| Booleano | `is_active` | `fl_active` |
| Estado/categoria | `record_status` | `st_record` ou `tp_record`, conforme a semântica definida pelo projeto |

## Árvore de decisão

Use esta sequência para escolher um nome claro; ela não impõe prefixos:

1. Nomear a entidade ou conceito ao qual o campo se refere.
2. Incluir papel ou unidade quando isso evitar ambiguidade.
3. Representar identificadores como texto quando não forem quantidades usadas em aritmética.
4. Explicitar se um estado ou categoria é mutável quando isso importar para interpretação.
5. Usar abreviações ou prefixos apenas se forem conhecidos pelos consumidores e consistentes no catálogo.

Identificadores externos, códigos postais e números de telefone normalmente devem ser texto, não medidas numéricas. Unidade, moeda e fuso ficam na documentação; incluí-los no nome apenas quando desambiguam grandezas diferentes. Evitar repetir a entidade no nome da coluna salvo ambiguidade.

## Problemas comuns

- Evitar nomes que só fazem sentido dentro de uma organização ou unidade sem contexto no schema.
- Evitar nomes genéricos sem qualificador quando não descrevem o papel, como `value`, `data`, `field` ou `status` em tabelas com mais de um conceito.
- Evitar repetição (`total_total`) e abreviações opacas; manter siglas reconhecidas pelo público consumidor.
- Não codificar fornecedor, cliente, sistema interno ou domínio de negócio no nome quando a coluna não for específica dessa origem.

## Exemplos

Claros em um catálogo `snake_case`: `record_id`, `source_record_id`, `created_at`, `total_amount`, `item_count`, `is_active`, `record_status`, `attribute_list`.

Pouco claros ou redundantes sem contexto: `value1`, `x`, `total_total`, `field`.

Semântica incerta é pendência: solicitar contexto em vez de escolher nome ou prefixo por suposição. Prefixos como `id_`, `dt_` ou `fl_` são exemplos de convenções possíveis, não requisitos universais.