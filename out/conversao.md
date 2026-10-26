# Conversor de SVG para PDF e PNG

Este script em Python varre o diretório atual em busca de arquivos `.svg` e gera versões em `.pdf` e `.png` em alta qualidade dentro de uma pasta chamada `exportados`.

## Pré-requisitos

Como o script utiliza o **Inkscape** para garantir a perfeita renderização das legendas e fontes, você precisa tê-lo instalado no seu sistema:

- **Windows / macOS / Linux:** Baixe e instale o Inkscape em [inkscape.org](https://inkscape.org/).
- Certifique-se de que o Inkscape está adicionado ao PATH do seu sistema (ou seja, acessível diretamente pelo terminal).

## Como executar

1. Coloque o script `converte_svg.py` na pasta onde estão os seus arquivos `.svg`.
2. Abra o terminal na pasta e execute:
```bash
python3 converte_svg.py
```