# Escolha entre SQL e Python

## Preferência de linguagem

Preferir SQL quando a transformação é expressável diretamente nas definições declarativas do pipeline. Considerar Python quando a tarefa realmente exige geração dinâmica a partir de metadados, biblioteca externa ou lógica condicional que não é clara em expressões SQL.

## API dependente de versão

A API Python de pipelines mudou ao longo das versões do Databricks Runtime (incluindo histórico de `dlt` e `pyspark.pipelines`). Não assumir import, alias, decorator ou helper atualmente suportado. Confirmar a documentação oficial da versão-alvo; se indisponível, marcar o exemplo como não validado e não apresentar snippet como código pronto para produção.

## Regras para transformações Python

- A função declarativa deve produzir o resultado esperado pelo framework, não executar gravações imperativas ou `MERGE` manual dentro da função.
- Selecionar leitura streaming ou batch de acordo com o contrato da origem.
- Preservar a mesma semântica de tipos, nulos, ordenação e chaves exigida no caminho SQL.
- Aplicar o padrão de nomes de coluna definido pelo projeto, se houver; não inventar nem presumir prefixos corporativos.

## Critério final

Escolha a forma mais simples que preserve comportamento e possa ser expressa declarativamente. Justifique o uso de Python quando a alternativa SQL suportada for insuficiente.