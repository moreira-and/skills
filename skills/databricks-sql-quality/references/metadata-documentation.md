# Documentação de Metadados

Comentários em catálogo, schema, tabela e coluna devem explicar os dados em linguagem de domínio, com contexto suficiente para pessoas e LLMs. A obrigatoriedade e o formato devem seguir as necessidades dos consumidores e as regras do catálogo, não um limite universal de tamanho. Escrever descrições específicas, coerentes com o dado e sem texto promocional ou boilerplate.

## Tabela ou view publicada

Descrever o conceito e a finalidade. Quando aplicável, incluir:

- o que o objeto representa e qual é a granularidade de uma linha;
- período coberto, filtros, regras de inclusão/exclusão e frequência de atualização;
- relações com outras entidades, limitações e estado do dado;
- termos de domínio e sinônimos importantes para busca e consulta.

## Coluna publicada

Descrever o conceito representado pelo campo, não apenas repetir o nome ou tipo. Quando relevante, incluir unidade/moeda, timezone, domínio de valores, condição de nulidade, regra de derivação e relação com a entidade da tabela. Usar termos e sinônimos do glossário do domínio quando fornecido.

## Exemplos

Exemplos neutros de comentários úteis:

- Catálogo: `Área de dados que reúne entidades e eventos usados para análise operacional.`
- Schema: `Conjunto de objetos que descrevem eventos observados e seu estado processado.`
- Tabela: `Um registro por evento recebido; inclui somente eventos aceitos pelo processo de ingestão.`
- Coluna: `Instante em que o evento ocorreu na origem, armazenado em UTC; nulo quando a origem não informa o horário.`
- Vago: `Tabela de dados.` ou `Valor.`

## Exceção

Se a plataforma ou consumidor não aceitar comentários, registrar a limitação em documentação adequada. Confirmar suporte da cláusula no objeto e versão de destino.

## Metadados para LLMs

Databricks documenta `COMMENT ON` para catálogos, schemas, tabelas e colunas. Para Genie, as recomendações oficiais destacam descrições de tabela/coluna claras; expressões SQL ajudam a definir semântica de métricas/filtros e consultas de exemplo esclarecem perguntas ambíguas. Comentários são contexto, não substituem um glossário ou definições semânticas quando o domínio exigir detalhe adicional.

Referências oficiais:

- [Databricks SQL: COMMENT ON](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-comment)
- [Databricks Genie: best practices](https://docs.databricks.com/aws/en/genie-agents/best-practices)