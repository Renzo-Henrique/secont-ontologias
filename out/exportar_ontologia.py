import os
import subprocess
from pathlib import Path
from typing import Optional
import rdflib
from rdflib.namespace import OWL, RDF, RDFS

_PREFIX_OUTPUT_DIR = "./diagramas"
_PREFIX_NUCLEO = "/nucleo"
_PREFIX_RECEITAS = "/receitas"
_PREFIX_DESPESAS = "/despesas"
_PREFIX_OUTPUT_DICIONARIO = "./dicionario_de_conceitos"

def exportar_diagramas_com_tonto_view(input_path: str, output_dir: Optional[str] = None, output_name: Optional[str] = None, view_file: Optional[str] = None):
    """
    Gera diagramas SVG a partir de um arquivo .tonto utilizando o tonto-view via npx.
    
    :param input_path: Caminho para o arquivo de entrada (.tonto)
    :param output_dir: Diretório onde o arquivo de saída será salvo (opcional)
    :param output_name: Nome personalizado para o arquivo de saída sem extensão (opcional)
    :param view_file: Caminho para o arquivo de arranjo .tontoview (opcional)
    """
    input_file = Path(input_path).resolve()

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_file}")

    # Define o diretório de saída padrão caso não seja fornecido (ex: diretório atual ou do arquivo)
    out_dir = Path(output_dir).resolve() if output_dir else Path.cwd()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Define o nome do arquivo de saída (usa o nome do arquivo .tonto por padrão se não especificado)
    base_name = output_name if output_name else input_file.stem
    svg_output = out_dir / f"{base_name}.svg"

    try:
        print(f"Processando visualização para: {input_file.name}")

        # Monta a base do comando
        cmd_parts = ["npx", "tonto-view", str(input_file), "--svg"]
        
        # Adiciona o arquivo de visualização (.tontoview) se fornecido
        if view_file and Path(view_file).exists():
            cmd_parts.extend(["--view", str(view_file)])

        print("Gerando arquivo SVG...")
        # Junta os comandos em uma string para rodar com shell=True
        cmd_str = " ".join([f'"{p}"' if " " in p else p for p in cmd_parts])
        
        with open(svg_output, "w", encoding="utf-8") as f_svg:
            subprocess.run(cmd_str, shell=True, stdout=f_svg, check=True, text=True)
            
        print(f"SVG salvo em: {svg_output}")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o tonto-view: {e}")
    except FileNotFoundError:
        print("Erro: O comando 'npx' não foi encontrado no PATH. Verifique se o Node.js está instalado.")

def exportarNucleo():
    exportar_diagramas_com_tonto_view(
                input_path="../src/nucleo/nucleo.tonto",
                output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_NUCLEO,
                view_file="../src/nucleo/views/nucleo.tontoview"
    )

def exportarReceitas():
    exportar_diagramas_com_tonto_view(
                input_path="../src/bases/receitas/base-receitas.tonto",
                output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_RECEITAS,
                view_file="../src/bases/receitas/views/versoes_da_view/base-receitas_SEM_atributos.tontoview"
        )
    exportar_diagramas_com_tonto_view(
            input_path="../src/bases/receitas/base-receitas.tonto",
            output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_RECEITAS,
            output_name="base-receitas-atributos",
            view_file="../src/bases/receitas/views/versoes_da_view/base-receitas_COM_atributos.tontoview"
        )


def exportarDespesas():
    exportar_diagramas_com_tonto_view(
                input_path="../src/bases/despesas/base-despesas.tonto",
                output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
                output_name="base-despesas",
                view_file="../src/bases/despesas/views/versoes_da_view/base-despesas.tontoview"
        )
    exportar_diagramas_com_tonto_view(
                input_path="../src/bases/despesas/base-despesas.tonto",
                output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
                output_name="base-despesas-atributos",
                view_file="../src/bases/despesas/views/versoes_da_view/base-despesas-atributos.tontoview"
        )



def exportar_ontologias_operacionais(src_dir: str = "../src", output_dir: str = "./ttl"):
    """
    Varre todos os arquivos .tonto na pasta especificada e converte cada um
    em arquivos .ttl alinhados ao gUFO salvos no diretório de saída.
    
    :param src_dir: Diretório raiz contendo os arquivos .tonto
    :param output_dir: Diretório onde os arquivos .ttl de saída serão salvos
    """
    root_path = Path(src_dir).resolve()
    out_dir_path = Path(output_dir).resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"Diretório de origem não encontrado: {root_path}")

    # Garante que o diretório de saída existe
    out_dir_path.mkdir(parents=True, exist_ok=True)

    # Busca todos os arquivos .tonto recursivamente dentro da pasta src
    tonto_files = list(root_path.glob("**/*.tonto"))

    if not tonto_files:
        print(f"Nenhum arquivo .tonto encontrado em: {root_path}")
        return

    try:
        print(f"Encontrados {len(tonto_files)} arquivos .tonto. Exportando para Turtle...")

        # Monta a lista de caminhos dos arquivos encontrados
        paths_str = [str(f) for f in tonto_files]

        # CORREÇÃO: Utilizar --out-dir=<dir> com '=' conforme sugerido pela mensagem de erro do tonto
        cmd_parts = ["npx", "tonto", "gufo"] + paths_str + [f"--out-dir={str(out_dir_path)}"]

        # Formata o comando para execução segura via shell
        cmd_str = " ".join([f'"{p}"' if " " in p else p for p in cmd_parts])

        subprocess.run(cmd_str, shell=True, check=True, text=True)
        print(f"Ontologias operacionais exportadas com sucesso para o diretório: {out_dir_path}")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao exportar as ontologias para Turtle: {e}")
    except FileNotFoundError:
        print("Erro: O comando 'npx' não foi encontrado no PATH. Verifique se o Node.js está instalado.")

def escapar_latex(texto: str) -> str:
  """Escapa caracteres especiais do LaTeX para evitar erros de compilação."""
  if not texto:
    return ""
  substituicoes = {
      "\\": r"\textbackslash{}",
      "&": r"\&",
      "%": r"\%",
      "$": r"\$",
      "#": r"\#",
      "_": r"\_",
      "{": r"\{",
      "}": r"\}",
      "~": r"\textasciitilde{}",
      "^": r"\textasciicircum{}",
  }
  for char, sub in substituicoes.items():
    texto = texto.replace(char, sub)
  # Normaliza quebras de linha e espaços múltiplos para manter a tabela limpa
  return " ".join(texto.split())


def gerar_dicionario_latex(
    caminho_ttl: str, caminho_saida: str, idioma_preferido: str = "pt"
):
  """Lê um arquivo .ttl usando rdflib, filtra estritamente instâncias de owl:Class

  e gera o arquivo de saída com as linhas da tabela LaTeX.
  """
  g = rdflib.Graph()
  g.parse(caminho_ttl, format="turtle")

  linhas_tabela = []

  # Filtra apenas entidades que são instâncias de owl:Class
  classes = set(g.subjects(RDF.type, OWL.Class))

  for entidade in sorted(classes, key=str):
    labels = list(g.objects(entidade, RDFS.label))
    comments = list(g.objects(entidade, RDFS.comment))

    def escolher_texto(literais):
      if not literais:
        return ""
      # Tenta priorizar o idioma escolhido (ex: 'pt', 'pt-br')
      for lit in literais:
        if (
            hasattr(lit, "language")
            and lit.language
            and idioma_preferido in lit.language.lower()
        ):
          return str(lit)
      # Fallback para o primeiro literal disponível
      return str(literais[0])

    label_str = escapar_latex(escolher_texto(labels))
    comment_str = escapar_latex(escolher_texto(comments))

    # Fallback caso a classe não tenha rdfs:label explícito
    if not label_str and isinstance(entidade, rdflib.URIRef):
      nome_uri = str(entidade).split("#")[-1].split("/")[-1]
      label_str = escapar_latex(nome_uri)

    # Formata a linha exatamente no padrão solicitado
    linha = f"{label_str} &\n{comment_str} \n\\\\ \\hline\n"
    linhas_tabela.append(linha)

  # Escreve o resultado no arquivo de saída
  with open(caminho_saida, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas_tabela))

  print(
      f"Arquivo '{caminho_saida}' gerado com sucesso ({len(linhas_tabela)}"
      " classes processadas)."
  )

def gerar_dicionarios():
   file_in = "nucleo"
   gerar_dicionario_latex(
      caminho_ttl=f"ttl/{file_in}.ttl", caminho_saida= f"{_PREFIX_OUTPUT_DICIONARIO}/{file_in}.tex"
  )
   file_in = "base-receitas"
   gerar_dicionario_latex(
      caminho_ttl=f"ttl/{file_in}.ttl", caminho_saida= f"{_PREFIX_OUTPUT_DICIONARIO}/{file_in}.tex"
  )
   file_in = "base-despesas"
   gerar_dicionario_latex(
      caminho_ttl=f"ttl/{file_in}.ttl", caminho_saida= f"{_PREFIX_OUTPUT_DICIONARIO}/{file_in}.tex"
  )

# Exemplo de uso:
if __name__ == "__main__":
    exportarNucleo()
    exportarReceitas()
    exportarDespesas()
    exportar_ontologias_operacionais()
    gerar_dicionarios()
    