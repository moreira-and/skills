# Streaming Tables

Esta referência descreve critérios de decisão e exemplos do legado. Confirme a sintaxe e o suporte de fontes na versão do Lakeflow alvo antes de usar exemplos em produção.

## Quando considerar

Considere streaming table quando a fonte é incremental (arquivos, Kafka ou Delta append-only) e a transformação pode processar os novos dados sem reler todo o histórico, por exemplo transformação linha a linha, filtro, limpeza ou agregação incremental simples.

Exemplo de forma declarativa para uma fonte tabular incremental:

```sql
CREATE OR REFRESH STREAMING TABLE sample_catalog.sample_schema.source_event
COMMENT 'Ingestão bruta da origem de eventos.'
AS SELECT *
FROM STREAM(sample_catalog.sample_schema.input_event);
```

Exemplo de leitura incremental de arquivos em storage:

```sql
CREATE OR REFRESH STREAMING TABLE sample_catalog.sample_schema.source_event
AS SELECT *
FROM STREAM read_files(
    '/Volumes/sample_catalog/sample_schema/sample_volume/input/',
    format => 'json'
);
```

## Pontos de decisão

- O uso de `STREAM` expressa leitura incremental no padrão de origem; confirmar a forma exigida pela fonte e pela versão.
- Uma origem lida como stream deve ser compatível com o modelo incremental. Updates/deletes na origem podem exigir outro objeto ou estratégia de CDC.
- Checkpoint e progresso de leitura são gerenciados pelo pipeline; não transportar automaticamente controles de offsets de jobs Structured Streaming.
- Várias origens para um alvo podem exigir flows separados; a sintaxe e o desenho de `APPEND FLOW`/`CREATE FLOW` devem ser confirmados na versão-alvo.
- Mudança aditiva de schema e mudança incompatível não têm o mesmo impacto; validar evolução de tipos/colunas e plano de recuperação antes de atualizar produção.

## Antipadrões comuns na migração

- Converter uma leitura incremental para leitura snapshot sem conferir o efeito no processamento.
- Levar limites de arquivos por trigger de job imperativo para uma definição declarativa sem necessidade comprovada.
- Usar tabela comum esperando incrementalidade sem o tipo e a declaração próprios de pipeline.

O formato exato dos exemplos não foi certificado para um runtime específico nesta implementação.