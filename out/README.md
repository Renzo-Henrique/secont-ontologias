# Automação de Exportação de Ontologias e Diagramas

Este diretório contém os scripts de automação em Python e as dependências necessárias para processar modelos ontológicos escritos na linguagem **Tonto** (utilizando o ecossistema `@nemo-ufes`). Ele automatiza a geração de diagramas visuais em formato vetorial (`.svg`) baseados em arquivos de arranjo (`.tontoview`) e a exportação das ontologias operacionais para o padrão semântico alinhado ao **gUFO** (`.ttl` / Turtle).

---


## ⚙️ Descrição dos Componentes Principais

### 1. `exportar_ontologia.py`

Script em Python responsável por orquestrar a execução das ferramentas de linha de comando do Tonto (`npx tonto-view` e `npx tonto gufo`). Ele realiza:

* **Geração de Diagramas SVG:** Varre os arquivos `.tonto` de origem e aplica visualizações customizadas (`.tontoview`) gerando diagramas limpos (com ou sem atributos, conforme o caso) salvos na pasta `diagramas/`.
* **Exportação gUFO Turtle:** Varre recursivamente os arquivos `.tonto` na pasta de origem e exporta cada ontologia no formato padrão semântico `.ttl` para a pasta `ttl/`.

### 2. Pasta `diagramas/`

Contém as representações visuais em formato vetorial (`.svg`) organizadas por subdomínios (`nucleo`, `receitas`, `despesas`). Estes arquivos são utilizados para documentação e inspeção visual das classes, relatórios e relacionamentos ontológicos.

### 3. Pasta `ttl/`

Contém os arquivos em formato **Turtle (`.ttl`)** gerados a partir do mapeamento oficial para o gUFO (`tonto gufo`). Eles representam formalmente as ontologias em OWL 2 DL prontas para serem consumidas por triplestores e ferramentas de raciocínio lógico (como o HermiT).

### 4. Configuração Node.js (`package.json`)

Gerencia as dependências de visualização e compilação de modelos do ecossistema Nemo-UFES, destacando-se o pacote `@nemo-ufes/tonto-visualizer-cli`.

---

## 🚀 Como Utilizar

### Pré-requisitos

* **Python 3.x** instalado.
* **Node.js** (versão 22 ou superior recomendada) instalado no ambiente.



### Instalação das dependências Node

Caso ainda não tenha instalado os pacotes do projeto, execute na raiz do diretório:

```bash
npm install

```

### Executando o script de exportação

Para rodar a automação completa (atualizando tanto os diagramas SVG quanto os arquivos Turtle `.ttl`), execute:

```bash
python3 exportar_ontologia.py

```