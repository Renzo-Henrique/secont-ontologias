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

## Processo de construção das ontologias

O processo de construção e modelagem das ontologias foi realizado de forma iterativa e padronizada para cada base de dados, seguindo as seguintes etapas:

- **Organização por pacotes:** Cada base de dados é mapeada e representada como um pacote individual dentro do ecossistema da ontologia.

- **Análise dos dicionários de dados:** Realiza-se o estudo preliminar das colunas e estruturas a partir dos dicionários de dados oficiais fornecidos por cada base.

- **Alinhamento com o MCASP:** Leitura e análise do [*Manual de Contabilidade Aplicada ao Setor Público (MCASP)*]() para identificação da semântica e dos significados dos conceitos centrais. O foco desta etapa é extrair a fundamentação conceitual por trás da entidade principal de cada base (como a *Receita Orçamentária* para a Base de Receitas e a *Despesa Orçamentária* para a Base de Despesas).

- **Consolidação do conhecimento do domínio:** Integra-se o conhecimento normativo/conceitual (obtido via MCASP) com a representação real dos dados contidos nas bases de dados, selecionando os arquivos e atributos verdadeiramente relevantes e atualizados.

- **Auditoria dos dados:** A informação dos dados e colunas dos arquivos é obtida pelo [portalTransparenciaGeracaoDeRelatorio](https://github.com/Renzo-Henrique/portalTransparenciaGeracaoDeRelatorio), em que são produzidos relatórios de "auditoria" da estrutura da base em colunas, metadados, dados por amostragem **E** pela análise total dos dados de arquivos específicos (normalmente utilizados os de 2025). As informações de dados são resumidas para mostrar quantidade de nulos, zeros, valores distintos, estatísticas numéricas e textuais. Também aponta possíveis colunas duplicadas por possuírem as mesmas estatísticas.

- **Formulação de questões de competência e modelagem em OntoUML:** A combinação do conhecimento de domínio com os metadados dos arquivos orienta a definição das Questões de Competência (QC) centrais de cada base. A partir delas, realiza-se a modelagem conceitual em **OntoUML** utilizando a linguagem textual **Tonto**.
  > **Nota de Escopo:** A ontologia possui viés predominantemente orientado às definições formais do MCASP. Contudo, devido a limitações de escopo horizontal, nem todos os conceitos periféricos de uma receita ou despesa são representados; similarmente, em termos de escopo vertical, não são detalhadas todos os conceitos atrelados à esses elementos, como o fato das classificações de uma despesa ou de uma receita não serem extremamente detalhadas.

- **Definição e refatoração do Pacote Núcleo (reuso):** Conceitos transversais e reutilizáveis em múltiplas bases são centralizados no pacote `nucleo` e refatorados para garantir consistência em todo o projeto:
  - Para representar papéis específicos atribuídos a entidades em contexturas distintas (ex.: papeis em relator), criam-se *roles* a partir da superclasse correspondente.
  - Para categorizar ou especificar semanticamente um conceito, utilizam-se *subkinds* derivados da superclasse.

- **Processo simplificado e refinamento contínuo:** Cada base passa inicialmente por uma versão simplificada da ontologia, permitindo um ciclo de refinamento progressivo que ajusta a modelagem aos dados reais sem perder a fidelidade ao conhecimento do domínio.
