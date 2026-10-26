# SECONT Ontologias

O propósito da ontologia é representar os conceitos relacionados aos dados publicados no Portal da Transparência do Poder Executivo do Estado do Espírito Santo, incluindo os conceitos administrativos, orçamentários, financeiros e contábeis necessários à interpretação dessas informações (*what*); de modo a estabelecer uma conceituação explícita e compartilhada que apoie a compreensão das bases por usuários humanos, a integração semântica entre diferentes conjuntos de dados e a posterior representação dos dados por meio de tecnologias da Web Semântica (*for what*); visando reduzir ambiguidades na interpretação dos dados, favorecer sua interoperabilidade semântica com dados internos e externos e ampliar as possibilidades de integração, consulta e reutilização automatizada das informações publicadas (*why*).


## Resumo dos pacotes

### Pacote nucleo

O pacote `nucleo` reúne as classes gerais e reutilizáveis da ontologia. Ele define conceitos fundamentais como `UnidadeGestora`, `PessoaFisica` e `PessoaJuridica`. Esse pacote funciona como base conceitual para os demais módulos e evita a duplicação de entidades constantemente referenciadas em bases de dados.

## Pacote bases
O pacote `bases` reúne as ontologias específicas para as bases do portal da transparência escolhidas para melhoria da qualidade dos dados.
- [base-receitas](https://dados.es.gov.br/dataset/portal-da-transparencia-receitas): Modela a **Receita orçamentária** como um **Documento Contábil** que é classificado de diversas formas e deve ter **Unidades Gestoras** atreladas.
- [base-despesas](https://dados.es.gov.br/dataset/portal-da-transparencia-despesas-execucao-orcamentaria-e-financeira): Modela a **Despesa** como...

## Como contribuir para a ontologia

A contribuição para esta ontologia deve seguir a lógica de modelagem adotada em Tonto, **recomendada a leitura do [repositório](https://github.com/nemo-ufes/tonto)**, e a organização do repositório em pacotes e arquivos. O processo de atualização deve manter consistência semântica, clareza conceitual e alinhamento com os dados públicos disponíveis.
