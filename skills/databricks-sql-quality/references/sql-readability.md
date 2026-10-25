# Legibilidade SQL

Recomendações comuns de leitura e revisão; adaptar ao guia de estilo efetivamente usado pelo projeto e registrar exceções relevantes.

## Formatação e projeção

- Keywords em maiúsculas; identificadores em minúsculas `snake_case`.
- Indentar com quatro espaços, sem tabs.
- Para mais de três colunas, listar uma coluna por linha.
- Evitar `SELECT *`: declarar as colunas necessárias explicitamente.
- Dar alias semântico a cada expressão derivada.
- Qualificar colunas com alias da fonte quando houver mais de uma fonte.

## CTEs e joins

- Uma responsabilidade por CTE; organizar da origem para tratamento, integração e resultado.
- Evitar CTE de passthrough como `SELECT * FROM cte_anterior`.
- Usar nomes descritivos `snake_case`, não `cte1`, `tmp` ou `aux`.
- Declarar tipos explícitos de join (`INNER JOIN`, `LEFT JOIN` etc.); não separar fontes com vírgulas.
- Usar condição `ON` e alias semântico de até quatro caracteres; evitar aliases genéricos como `a`, `b`, `t1`.

## Expressões

- Preferir `QUALIFY` para filtrar window functions quando a sintaxe e o caso de uso suportarem.
- Usar `UNION ALL` por padrão; justificar `UNION` com comentário quando a remoção de duplicatas for intencional.
- Em `CASE` extenso, colocar `WHEN`/`THEN` em linhas separadas e alinhadas.
- Em `WHERE` com mais de duas condições, usar uma condição por linha e colocar o operador lógico no início da linha.
- Comentários devem explicar decisão de negócio, exceção ou justificativa técnica; não narrar sintaxe óbvia.

Estas são recomendações, não uma política obrigatória de qualquer empresa. Verificar gramática da versão SQL de destino antes de aplicar recursos específicos.