# Welcome to your new Tonto project: {{projectName}}!

This is a sample project to help you get started with Tonto.
# secont-ontologias


# Duvidas
- Quando criar um tipo de dado específico para atributos do tipo número? Suspeito que seja quando seguem um determinado padrão
- DividaAtiva é necessário ser modelado, tendo em vista que só possuem dividas datadas de 2015?
- Em quais casos a descrição de uma classe na verdade é a da relação que ela possui?

1) Cada arquivo com nome diferente (excluindo o ano dos arquivos) recebe um arquivo .tonto para especifica-lo

2) Obter do dicionário de dados os atributos com nomes similares e transformá-los em *kind* para serem a primeira reificação de classes que agrupam atributos similares. Essa etapa transforma os tipos de atributos nos equivalentes aos tipos suportados da linguagem tonto.
Atributos gerais são agrupados em um *relator* específico do nome da base, exemplo de nomenclatura para a base "Receitas": ReceitasReificada

3) Obter dos arquivos publicados os atributos que não estão no dicionário de dados e marcá-los para análise detalhada posterior para verificar o tipo que será atribuído e o própria descrição do conceito. Em primeira análise, esses atributos recebem o tipo string

4) Conectar o *<base>Reificada* com as classes criadas em relações de mediação no seguinte padrão de multiplicidade: *<base>Reificada* [0..*] -- [1] *<classeCriada>*
Esse padrão de multiplicidade segue os conformes da OntoUML, visto que se fosse multiplicidade mínima 1 de origem na *<base>Reificada*, a *<classeCriada>* ser um *kind* não seria correta ontologicamente pelo *kind* ter que depender de uma relação de mediação para existir, o que não pode ser possível.
Caso seja necessário, diferenciar relações que se referem a mesma entidade com nomenclatura diferente se referindo ao papel que a relação possui. Por exemplo, em receitas tem a UnidadeGestora em que a receita é emitida e a UnidadeGestora que emite a receita, portanto os respectivos nomes de relação ficam *emitidaPara* e *emitidaPor*

5) Realizar a correção dos tipos de atributos que foram identificados como errados após análise. A análise envolve em verificar se os tipos descritos estão corretos de acordo com os arquivos .csv disponibilizados publicamente na base
Nessa etapa são criados tipos de dados específicos para cada código/identificador utilizado nas classes para que na operalização da ontologia facilite a criação de constraints que verificam se o código/identificador está correto, o padrão criado se torna: 

// Tipo de dado criado
datatype *<NomeDoCodigo>* specializes string

// Atributo dentro da classe
codigo: *<NomeDoCodigo>* [1] {const}

Nota-se que os códigos se tornam especializações de string para minimizar a ocorrência de erros de tipos, uma verificação de certos códigos especializarem outros tipos será feita posteriormente.