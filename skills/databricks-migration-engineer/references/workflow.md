# Fluxo de migração

Cada etapa só termina ao cumprir seu critério de saída.

## 1. Inventariar

- Liste origens, destinos, dependências, regras de negócio, chaves, ordenação, latência esperada, agenda, consumidores e ambiente.
- Se faltar chave, ordenação, latência, responsável ou ambiente, pergunte; não presuma, sobretudo em CDC e deduplicação.
- **Saída**: inventário com cobertura e pendências.

## 2. Planejar

- Mapeie cada decisão à regra local aplicável, com link: processo em `pyspark-to-lakeflow`, objetos e CDC em `lakeflow-pipelines`, nomes e tipos em `databricks-sql-quality`.
- Registre divergências entre regra local e prática geral e as premissas onde a regra for omissa.
- Aguarde aprovação antes de mudar identificadores que afetem consumidores.
- **Saída**: plano com regras citadas, divergências e premissas.

## 3. Converter

- Preserve regras, tipos, nulos, desempates, chaves, sequenciamento e comportamento incremental; documente qualquer diferença.
- Use as skills de regras como fonte; não reescreva aqui o conteúdo técnico delas.
- **Saída**: artefatos convertidos e lista de diferenças.

## 4. Validar

- Separe verificação estática (revisão, heurísticas) de execução real no workspace de teste.
- Marque como "não validada" a compatibilidade de versão ou sintaxe sem fonte oficial confirmada.
- Sem acesso ao workspace, entregue só o resultado estático e diga que a validação real está pendente.
- **Saída**: evidências e itens não validados.

## 5. Relatar

- Preencha o [modelo de relatório](report-template.md).
- **Saída**: relatório completo, com riscos residuais.

## Lotes

- Divida cargas grandes em unidades revisáveis (por job, tabela ou pipeline).
- Ao fim de cada lote, informe o que foi feito, o que falta e o que depende de decisão.
- Mantenha a mesma estrutura de relatório em todos os lotes.

## Casos de borda

- **Origem não PySpark** (scripts SQL, ferramentas de ETL): diga quais etapas se aplicam e que a conversão está fora da cobertura das regras locais.
- **Regra local omissa**: aplique prática de mercado e registre como premissa.
- **Regras locais em conflito**: exponha o conflito e peça decisão.
- **Versão-alvo desconhecida**: marque como "não validada".
