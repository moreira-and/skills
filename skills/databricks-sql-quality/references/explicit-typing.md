# Tipagem Explícita

Deixar claro o contrato de tipos dos dados publicados. Quando o formato do objeto permitir, declarar o schema junto à definição facilita leitura, validação e integração; seguir também as regras de schema efetivamente definidas para o projeto.

## Regras

- Preferir declaração explícita de tipos em contratos estáveis e objetos publicados quando suportado pelo tipo de objeto.
- Usar `CAST` para adequar expressões e evitar coerções implícitas inesperadas.
- Não exigir uma forma única de tipagem para todo projeto; seguir as regras de schema e compatibilidade do consumidor.
- Confirmar a gramática compatível com o objeto Lakeflow e a versão Databricks antes de publicar sintaxe operacional.

## Exemplo de intenção

Exemplo de schema explícito:

```sql
CREATE OR REPLACE TABLE sample_record (
    record_id BIGINT,
    created_at TIMESTAMP
)
AS
SELECT
    CAST(source_id AS BIGINT),
    event_timestamp
FROM source_record;
```

Evite depender somente de casts no SELECT quando o consumidor precisa de um contrato de schema estável. Validar a sintaxe no dialeto e versão em uso.