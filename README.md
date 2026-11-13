# OPTES - Ontologia do Portal da Transparência do ES

O propósito da ontologia é representar os conceitos relacionados aos dados publicados no Portal da Transparência do Poder Executivo do Estado do Espírito Santo, incluindo os conceitos administrativos, orçamentários, financeiros e contábeis necessários à interpretação dessas informações (*what*); de modo a estabelecer uma conceituação explícita e compartilhada que apoie a compreensão das bases por usuários humanos, a integração semântica entre diferentes conjuntos de dados e a posterior representação dos dados por meio de tecnologias da Web Semântica (*for what*); visando reduzir ambiguidades na interpretação dos dados, favorecer sua interoperabilidade semântica com dados internos e externos e ampliar as possibilidades de integração, consulta e reutilização automatizada das informações publicadas (*why*).


## Resumo dos pacotes
A arquitetura da ontologia é modularizada em pacotes independentes que separam conceitos transversais das especificidades de cada conjunto de dados publicado no Portal da Transparência, promovendo reuso e extensibilidade:

### Pacote nucleo

O pacote `nucleo` atua como o alicerce conceitual e estrutural do ecossistema da ontologia. Ele centraliza entidades transversais que não são específicas de conjuntos de dados, pois podem ser compartilhadas por múltiplos conjuntos de dados. Isso evita redundâncias e garante alinhamento semântico entre os módulos. Entre os principais domínios conceituais modelados no núcleo estão:

* **Estrutura Administrativa e Institucional:** `EntidadePublica`, `OrgaoPublico`, `UnidadeDeOrgaoPublico`, `OrgaoPublicoOrcamentario`, `UnidadeOrcamentaria` e `UnidadeGestora`.


* **Atores e Instituições:** `PessoaFisica`, `PessoaJuridica`, o subtipo `Banco` e estruturas de anonimização de dados pessoais (`DadosPessoaisAnonimizados` e `DadosPessoaisAnonimizadosExpandido`).


* **Recorte Territorial:** Hierarquia geográfica composta por `Regiao`, `MicroRegiao` e `Municipio`.


* **Instrumentos e Classificações Transversais:** `Convenio`, `PoderDaFederacao`, `EsferaOrcamentaria` e `FonteOrcamentaria`.



## Pacote bases
O pacote `bases` contém as ontologias de domínio específicas para cada conjunto de dados selecionado do Portal da Transparência. Cada módulo importa o pacote `nucleo` e especializa seus conceitos por meio de *roles*, *roleMixins* e *subkinds* para capturar o contexto específico das bases de dados:

### [base-receitas](https://dados.es.gov.br/dataset/portal-da-transparencia-receitas): 
Modela o domínio da **Receita Orçamentária** (`ReceitaOrcamentaria`) e suas classificações. A ontologia representa:

* **Registro de Receita**: O registro formal da receita (`RegistroDeReceitaOrcamentaria`) e os respectivos valores monetários brutos, líquidos e de dedução (`ValorAtreladoNaReceita`).


* **Unidade Gestora:** Os papéis desempenhados pelas unidades gestoras na operação (`UnidadeGestoraEmitenteDeReceita` e `UnidadeGestoraBeneficiadaDeReceita`) e as relações materiais derivadas (`emitidaPor` e `emitidaPara`).


* **Classificações:** As estruturas de classificação contábil e orçamentária por meio do relator `ClassificacaoDoRegistroDeReceitaOrcamentaria`, integrando `NaturezaDaReceita`, `FonteDaReceita` e `ContaContabil`.

### [base-despesas](https://dados.es.gov.br/dataset/portal-da-transparencia-despesas-execucao-orcamentaria-e-financeira): 
Modela o domínio da **Despesa Orçamentária** (`DespesaOrcamentaria`) no escopo de execução, classificação e vigência de uma despesa. A ontologia contempla:

* **Estágios da Execução:** Partição disjunta e completa dos estágios legais de execução da despesa (`DespesaDeEmpenho`, `DespesaDeLiquidacao` e `DespesaDePagamento`), além da distinção temporal entre despesas pagas no exercício vigente (`DespesaDeExercicioVigente`) e inscrições em Restos a Pagar (`DespesaDeExercicioAnterior`), modeladas via eventos de transição (`TerminoDoExercicioVigenteDaDespesa` e `CriacaoDeDespesaNaoPaga`).


* **Registros de uma Despesa:** Especialização de `RegistroDeDespesaOrcamentaria` em quatro tipos de arquivos publicados na base de despesas: `RegistroDeDespesa`, `RegistroDeRestosAPagar`, `RegistroDeOrcamentoDeDespesa` e `RegistroDeOrcamentoDeExecucao`, cada qual com seus respectivos dados.


* **Classificações:** Articulação entre as classificações institucional (`ClassificadorInstitucionalDeDespesa`), funcional (`ClassificadorFuncionalDeDespesa`), programática (`ClassificadorPorEstruturaProgramaticaDeDespesa`), por natureza (`ClassificadorPorNaturezaDeDespesa`), por fonte de recursos (`FonteDaDespesa`) e por esfera orçamentária (`EsferaOrcamentariaNaDespesa`).

## Como contribuir para a ontologia

A contribuição para esta ontologia deve seguir a lógica de modelagem adotada em Tonto, **recomendada a leitura do [repositório](https://github.com/nemo-ufes/tonto)**, e a organização do repositório em pacotes e arquivos. Toda atualização deve preservar a consistência semântica com a ontologia de fundamentação UFO/OntoUML, manter clareza conceitual nas anotações (`@pt-br` e referências normativas) e assegurar alinhamento estrito com os dados públicos disponíveis do portal da transparência do ES.

## Processo de construção da ontologia

O desenvolvimento dos pacotes da ontologia segue uma abordagem iterativa, incremental e orientada tanto pela fundamentação normativa quanto pela evidência dos dados reais publicados no portal. O fluxo metodológico compreende as seguintes etapas:

### 1. Estruturação Modular e Organização por Pacotes

Antes de iniciar a modelagem detalhada, o escopo do Portal da Transparência é segmentado por conjuntos de dados temáticos (como Receitas e Despesas). Cada base é isolada em um pacote próprio dentro de `bases`, mantendo acoplamento fraco entre os domínios e convergindo dependências comuns para o pacote `nucleo`. Essa organização facilita a manutenção independente, o versionamento e a futura expansão para novas bases governamentais.

### 2. Levantamento Preliminar e Análise dos Dicionários de Dados

Para cada base selecionada, realiza-se o mapeamento inicial dos esquemas tabulares (arquivos CSV/dados abertos) e de seus respectivos dicionários de dados oficiais. Nesta etapa, identificam-se os nomes técnicos das colunas, os tipos primitivos esperados, as chaves de ligação entre arquivos (como `Despesas`, `RestosAPagar`, `OrcamentosDespesa` e `OrcamentosExecucoes`) e as descrições administrativas fornecidas pelos órgãos mantenedores.

### 3. Auditoria Estatística dos Dados

Como os dicionários de dados das bases não estão totalmente atualizados com o que a base possui, tendo ambiguidades ou colunas obsoletas, realiza-se uma auditoria sistemática dos arquivos reais por meio da ferramenta [portalTransparenciaGeracaoDeRelatorio](https://www.google.com/search?q=https://github.com/Renzo-Henrique/portalTransparenciaGeracaoDeRelatorio). O processo envolve:

* **Análise por amostragem e varredura integral:** Avaliação estrutural completa de recortes anuais representativos (priorizando exercícios recentes, como 2025).


* **Diagnóstico de qualidade e preenchimento:** Levantamento da taxa de valores nulos, ocorrência de zeros, cardinalidade de valores distintos, distribuições numéricas e padrões textuais.


* **Detecção de anomalias e redundâncias:** Identificação de colunas duplicadas (com perfis estatísticos idênticos), campos sem utilidade prática documentada (como códigos legados sem preenchimento efetivo) e regras implícitas de negócio que não constam nos dicionários oficiais.



### 4. Fundamentação Normativa e Alinhamento com o MCASP e Legislação

Paralelamente à análise dos dados, realiza-se o estudo aprofundado da legislação financeira e contábil brasileira — com destaque para o *[Manual de Contabilidade Aplicada ao Setor Público (MCASP)](https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-contabilidade-aplicada-ao-setor-publico-mcasp-1)*, a Lei nº 4.320/1964 e portarias da Secretaria do Tesouro Nacional (STN) e da Secretaria de Orçamento Federal (SOF). O objetivo é extrair a semântica formal por trás dos conceitos centrais (como na despesa a distinção entre os estágios de empenho, liquidação e pagamento, a inscrição em restos a pagar e a estrutura das classificações orçamentárias), documentando essas definições diretamente nas entidades da ontologia.

### 5. Consolidação Semântica e Definição de Escopo

Nesta fase, confronta-se o modelo normativo ideal (obtido via MCASP e leis) com a realidade operacional revelada pela auditoria dos dados. Define-se o que será efetivamente representado, filtrando arquivos e atributos relevantes e estabelecendo fronteiras claras de modelagem:

> **Nota sobre Delimitação de Escopo (Horizontal e Vertical):**
> A ontologia possui viés predominantemente orientado às definições formais do MCASP. Contudo, devido a decisões pragmáticas de **escopo horizontal**, nem todos os conceitos periféricos associados a uma receita ou despesa são incorporados no modelo inicial. Da mesma forma, em termos de **escopo vertical**, evita-se o aprofundamento excessivo em subníveis hiperdetalhados de determinadas classificações ou etapas preliminares de planejamento quando estes não agregam valor direto às consultas principais ou não possuem lastro consistente nos dados publicados.

### 6. Formulação de Questões de Competência (QC)

A interseção entre o conhecimento jurídico-contábil e os metadados auditados orienta a elaboração das **Questões de Competência (QCs)** de cada módulo. As QCs formalizam as perguntas de negócio e transparência pública que a ontologia deve ser capaz de responder (por exemplo: *quais unidades gestoras tiveram mais despesas*, ou *como uma despesa empenhada não paga se transforma para restos a pagar ao fim do exercício*), servindo como critério objetivo de validação durante e após a modelagem.

### 7. Modelagem Conceitual em OntoUML via Linguagem Tonto

Com base nas QCs, constrói-se o modelo conceitual fundamentado na *Unified Foundational Ontology* (UFO/OntoUML), codificado textualmente em **Tonto**. Nessa etapa, aplicam-se rigorosamente os estereótipos ontológicos adequados à natureza de cada conceito:

* **`kind` e `subkind`:** Para entidades com princípio de identidade próprio e suas especializações rígidas (ex.: `DespesaOrcamentaria`, `ReceitaOrcamentaria`).


* **`phase`:** Para estados intrínsecos e temporais pelos quais uma entidade transita ao longo de seu ciclo de vida (ex.: `DespesaDeEmpenho`, `DespesaDeLiquidacao` e `DespesaDePagamento`).


* **`role` e `roleMixin`:** Para papéis relacionais assumidos por entidades em contextos específicos (ex.: `UnidadeGestoraEmitenteDeReceita`, `OrgaoPublicoOrcamentarioNaDespesa`, `FonteDaDespesa`).


* **`category`:** Para agrupar propriedades essenciais compartilhadas por entidades de diferentes naturezas (ex.: estruturas de classificação funcional, programática e por natureza).


* **`relator`, `event` e `situation`:** Para reificar relações complexas que conectam múltiplos participantes (como os registros orçamentários e suas classificações) e capturar mudanças de estado no tempo (como a criação de despesas não pagas no encerramento do exercício).


* **`datatype`:** Para estruturar atributos compostos, como blocos de valores monetários, dados de licitação e retenções.



### 8. Extração, Generalização e Refatoração do Pacote `nucleo`

À medida que diferentes bases são modeladas, identifica-se a recorrência de conceitos transversais (como órgãos, unidades gestoras, municípios, pessoas físicas/jurídicas, convênios e fontes de recursos). Esses elementos são extraídos dos pacotes específicos, generalizados e consolidados no pacote `nucleo`. Nas ontologias das bases, os conceitos originais são então refatorados para especializar as classes do núcleo para manter a dependência dos pacotes indo para núcleo e não o contrário.

### 9. Ciclos de Evolução da ontologia e Análises Complementares

Cada ontologia nasce a partir de uma versão simplificada que cobre os conceitos essenciais da base e passa por ciclos sucessivos de revisão. Sempre que surgem dúvidas sobre cardinalidades, opcionalidade de relacionamentos ou comportamento de chaves nos arquivos do portal, executam-se análises exploratórias pontuais nos dados brutos para ajustar restrições (`const`, multiplicidades `[0..1]`, `[1..*]`, conjuntos de generalização `disjoint`/`complete`) sem comprometer o rigor conceitual do domínio.

