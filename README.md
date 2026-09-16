# SECONT Ontologias

O propósito da ontologia é representar os conceitos relacionados aos dados publicados no Portal da Transparência do Poder Executivo do Estado do Espírito Santo, incluindo os conceitos administrativos, orçamentários, financeiros e contábeis necessários à interpretação dessas informações (*what*); de modo a estabelecer uma conceituação explícita e compartilhada que apoie a compreensão das bases por usuários humanos, a integração semântica entre diferentes conjuntos de dados e a posterior representação dos dados por meio de tecnologias da Web Semântica (*for what*); visando reduzir ambiguidades na interpretação dos dados, favorecer sua interoperabilidade semântica com dados internos e externos e ampliar as possibilidades de integração, consulta e reutilização automatizada das informações publicadas (*why*).


## Resumo dos pacotes

### Pacote núcleo

O pacote `nucleo` reúne as classes gerais e reutilizáveis da ontologia. Ele define conceitos fundamentais como `UnidadeGestora`, `PessoaFisica` e `PessoaJuridica`, além de datatypes específicos para identificação, como `CodigoUnidadeGestora`, `Cpf` e `Cnpj`. Esse pacote funciona como base conceitual para os demais módulos e evita a duplicação de entidades constantemente referenciadas em bases de dados.

### Pacote receitas

O pacote `receitas` concentra os conceitos relacionados à classificação e registro das receitas públicas. Entre os elementos principais estão `ContaContabil`, `NaturezaReceita`, `CategoriaReceita`, `OrigemReceita`, `EspecieReceita`, `RubricaReceita`, `AlineaReceita`, `SubAlineaReceita`, `FonteReceita`, `GrupoFonteReceita` e `DetalhamentoFonteReceita`. Também inclui o relator `ReceitaReificada`, responsável por capturar as ocorrências de uma receita e as relações de mediação com as entidades classificatórias e com as unidades gestoras envolvidas.

Adicionalmente, o pacote contempla a extensão de dívida ativa, tratando as relações entre pessoas e registros patrimoniais/tributários. Esse conjunto permite representar tanto a estrutura da receita quanto o contexto em que ela é emitida, arrecadada e vinculada às unidades gestoras relevantes.

## Como contribuir para a ontologia

A contribuição para esta ontologia deve seguir a lógica de modelagem adotada em Tonto, **recomendada a leitura do [guia](https://nemo-ufes.github.io/Tonto/)**, e a organização do repositório em pacotes e arquivos. O processo de atualização deve manter consistência semântica, clareza conceitual e alinhamento com os dados públicos disponíveis.

### 1. Entender o domínio antes de editar a ontologia

Antes de inserir novos conceitos ou alterar relações, é necessário revisar os dados de origem, os dicionários de dados e os arquivos CSV que sustentam o domínio e a documentação criada a partir da metodologia SABiOx. A análise deve identificar:

- atributos repetidos em diferentes bases;
- termos equivalentes ou ambíguos;
- códigos e identificadores que exigem tipagem específica;
- relações relevantes entre entidades.

Essa etapa evita que a ontologia incorpore termos inconsistentes ou classes redundantes.

### 2. Organizar a modelagem por pacote e por arquivo

Cada base deve ser mapeado em um diretório e cada arquivo nomeado deve possuir um .tonto específico, preservando a divisão conceitual do repositório. Quando um conceito for mais geral e reutilizável, ele deve ser colocado no pacote núcleo e, se necessário, especializado em pacotes específicos. Isso favorece a reutilização e reduz duplicação de entidades.

### 3. Tipar corretamente identificadores e códigos

Após a análise inicial, atributos que representem códigos, identificadores ou valores de referência devem receber tipos específicos, através de datatypes que especializam string. Essa prática reduz erros de atribuição e facilita a criação de constraints para validação semântica na operacionalização da ontologia.

### 4. Documentar e manter a consistência do modelo

Toda contribuição deve:

- manter descrições em português com clareza e precisão seguindo o dicionário da base de dados sempre que possível;
- usar labels e descriptions adequados para cada conceito;
- preservar a convenção de nomenclatura do projeto;
- verificar se a classe ou atributo já existe antes de criar uma nova entidade;
- manter os arquivos organizados e coerentes com a estrutura do pacote.

### 5. Fluxo recomendado para contribuição

O fluxo sugerido para ampliar ou ajustar a ontologia é:

1. localizar o pacote adequado;
2. revisar a estrutura já existente e os conceitos relacionados;
3. identificar se a mudança deve afetar o núcleo ou um pacote específico;
4. editar o arquivo .tonto correspondente;
5. ajustar labels, descriptions, relações e tipos;
6. validar a consistência conceitual e semântica;
7. registrar a alteração em commit e, quando necessário, abrir pull request com descrição clara do que foi modificado.

Esse processo garante que a ontologia evolua de forma coerente com os princípios de modelagem em Tonto e com os objetivos do projeto SECONT.

## Recomendação de passo a passo de construção dos arquivos .tonto
0) Caso um kind se torne parte do pacote núcleo, o recomendado é criar uma especialização da classe para utiliza-la no pacote específico.

1) Cada arquivo com nome diferente (excluindo o ano dos arquivos) recebe um arquivo .tonto para especifica-lo

2) Obter do dicionário de dados os atributos com nomes similares e transformá-los em *kind* para serem a primeira reificação de classes que agrupam atributos similares. Essa etapa transforma os tipos de atributos nos equivalentes aos tipos suportados da linguagem tonto.
Atributos gerais são agrupados em um *relator* específico do nome da base, exemplo de nomenclatura para a base "Receitas": ReceitasReificada

3) Obter dos arquivos publicados os atributos que não estão no dicionário de dados e marcá-los para análise detalhada posterior para verificar o tipo que será atribuído e o própria descrição do conceito. Em primeira análise, esses atributos recebem o tipo string

4) Conectar o *<base>Reificada* com as classes criadas em relações de mediação no seguinte padrão de multiplicidade: *<base>Reificada* [0..*] -- [1] *<classeCriada>*
Esse padrão de multiplicidade segue os conformes da OntoUML, visto que se fosse multiplicidade mínima 1 de origem na *<base>Reificada*, a *<classeCriada>* ser um *kind* não seria correta ontologicamente pelo *kind* ter que depender de uma relação de mediação para existir, o que não pode ser possível.
Caso seja necessário, diferenciar relações que se referem a mesma entidade com nomenclatura diferente se referindo ao papel que a relação possui. Por exemplo, em receitas tem a UnidadeGestora em que a receita é emitida e a UnidadeGestora que emite a receita, portanto os respectivos nomes de relação ficam *emitidaPara* e *emitidaPor*

5) Realizar a correção dos tipos de atributos que foram identificados como errados após análise. A análise envolve em verificar se os tipos descritos estão corretos de acordo com os arquivos .csv disponibilizados publicamente na base
Nessa etapa são criados tipos de dados específicos para cada código/identificador utilizado nas classes para que na operalização da ontologia facilite a criação de constraints que verificam se o código/identificador está correto, o padrão criado se torna: 

```
# Tipo de dado criado
datatype <NomeDoCodigo> specializes string

# Atributo dentro da classe
codigo: <NomeDoCodigo> [1] {const}

# Exemplo:
datatype Cpf specializes string
kind PessoaFisica {
    cpf: Cpf [1] {const}
}
```
Nota-se que os códigos se tornam especializações de string para minimizar a ocorrência de erros de tipos, uma verificação de certos códigos especializarem outros tipos será feita posteriormente.

## Documentação da ontologia


### Convertendo .svg para pdf
Comando para converter os arquivos .svg gerados dos plantUML para colocar em relatórios e artigos

```
for f in *.svg; do
    inkscape "$f" --export-type=pdf --export-filename="${f%.svg}.pdf"
done
```