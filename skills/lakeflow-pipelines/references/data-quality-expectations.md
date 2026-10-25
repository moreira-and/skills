# Expectations de Qualidade de Dados

Use expectations para associar regras de qualidade a um pipeline e tornar explícito o destino dos registros que violam a regra. Confirme a gramática aceita pela versão Lakeflow antes de usar a sintaxe abaixo.

```sql
CREATE OR REFRESH STREAMING TABLE sample_catalog.sample_schema.validated_record
(
    CONSTRAINT record_id_present EXPECT (record_id IS NOT NULL),
    CONSTRAINT event_time_present EXPECT (event_timestamp IS NOT NULL) ON VIOLATION DROP ROW,
    CONSTRAINT amount_nonnegative EXPECT (amount >= 0) ON VIOLATION FAIL UPDATE
)
AS SELECT * FROM STREAM(sample_catalog.sample_schema.source_record);
```

## Efeitos de violação

| Comportamento | Efeito pretendido |
|---|---|
| Sem ação explícita | Mede/registra a violação e mantém a linha, conforme o comportamento de referência; confirmar versão |
| Drop row | Descarta linha violadora e registra a métrica |
| Fail update | Interrompe a atualização por violação; reservar para invariantes críticas e avaliar impacto operacional |

## Boas práticas

- Nomear constraints com o significado da regra; seus nomes podem aparecer em métricas/eventos.
- Preferir observação ou descarte para problemas de dados pontuais; usar falha do update apenas quando interromper o pipeline for a resposta correta a uma quebra estrutural.
- Combinar regras com `AND` apenas quando fizer sentido e não for necessário medir cada regra separadamente.
- Expectations não substituem contrato de schema e tipos.
- Registrar a decisão de negócio para cada regra e o efeito esperado sobre dados e continuidade do pipeline.