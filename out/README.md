# Automação de exportação de artefatos da ontologia

Este diretório contém os scripts de automação em Python e as dependências necessárias para processar modelos ontológicos escritos na linguagem **Tonto**. Ele automatiza a geração de diagramas visuais em formato vetorial (`.svg`) baseados em arquivos de arranjo (`.tontoview`), a exportação das ontologias operacionais para o padrão semântico alinhado ao **gUFO** (`.ttl` / Turtle) e a geração dos dicionários de conceitos em LaTeX para serem usados na documentação da ontologia.

---


## ⚙️ Descrição dos Componentes Principais

### 1. `exportar_ontologia.py`

Script em Python responsável por orquestrar a execução das ferramentas de linha de comando do Tonto (`npx tonto-view` e `npx tonto gufo`) e processar os artefatos. Ele realiza:

* **Geração de Diagramas SVG:** Varre os arquivos `.tonto` de origem e aplica visualizações customizadas (`.tontoview`) gerando diagramas limpos (com ou sem atributos, conforme o caso) salvos na pasta `diagramas/`.


* **Exportação gUFO Turtle:** Varre recursivamente os arquivos `.tonto` na pasta de origem e exporta cada ontologia no formato padrão semântico `.ttl` para a pasta `ttl/`.


* **Geração do Dicionário de Conceitos (LaTeX):** Processa e exporta os conceitos ontológicos estruturados para arquivos `.tex` na pasta `dicionario_de_conceitos/`.



### 2. Pasta `diagramas/`

Contém as representações visuais em formato vetorial (`.svg`) organizadas por subdomínios (`nucleo`, `receitas`, `despesas`). Estes arquivos são utilizados para documentação e inspeção visual das classes, relatórios e relacionamentos ontológicos.

### 3. Pasta `ttl/`

Contém os arquivos em formato **Turtle (`.ttl`)** gerados a partir do mapeamento oficial para o gUFO (`tonto gufo`). Eles representam formalmente as ontologias em OWL 2 DL prontas para serem consumidas por triplestores e ferramentas de raciocínio lógico (como o HermiT).

### 4. Pasta `dicionario_de_conceitos/`

Contém os arquivos em formato **LaTeX (`.tex`)** gerados automaticamente, servindo como documentação textual e dicionário formal dos conceitos das ontologias.

### 5. Configuração Node.js (`package.json`)

Gerencia as dependências de visualização e compilação de modelos **Tonto**.

---

## 🚀 Como Utilizar

### Pré-requisitos

* **Python 3.x** instalado.
* **Node.js** (versão 22 ou superior recomendada) instalado no ambiente.
* **rdflib** biblioteca python para leitura de arquivos rdf
* **cairosvg** biblioteca python para conversão de arquivos .svg para pdf


### Configuração do Ambiente Virtual Python

É altamente recomendado o uso de um ambiente virtual Python para isolar as dependências do projeto. Na raiz do diretório, execute:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```


### Instalação das Dependências Node

Caso ainda não tenha instalado os pacotes do ecossistema Node, execute na raiz do diretório:

```bash
npm install

```

### Executando o Script de Exportação

Para rodar a automação completa (atualizando os diagramas SVG, os arquivos Turtle `.ttl` e os dicionários de conceitos em LaTeX `.tex`), execute:

```bash
python3 exportar_ontologia.py

```