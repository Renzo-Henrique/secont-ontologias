import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import rdflib
from rdflib.namespace import OWL, RDF, RDFS, DCTERMS, VANN

_PREFIX_OUTPUT_DIR = "./diagramas"
_PREFIX_NUCLEO = "/nucleo"
_PREFIX_RECEITAS = "/receitas"
_PREFIX_DESPESAS = "/despesas"
_PREFIX_OUTPUT_DICIONARIO = "./dicionario_de_conceitos"

def converter_svg_para_pdf(svg_path: Path, pdf_path: Path) -> None:
    """
    Converte um SVG em PDF, preservando o formato vetorial.

    Prioriza o Inkscape. Caso não esteja instalado, tenta usar o CairoSVG
    (biblioteca Python).
    """
    inkscape = shutil.which("inkscape")

    if inkscape:
        subprocess.run(
            [
                inkscape,
                str(svg_path),
                "--export-type=pdf",
                f"--export-filename={pdf_path}",
            ],
            check=True,
            text=True,
        )
        return

    try:
        import cairosvg
    except ImportError as exc:
        raise RuntimeError(
            "Não foi possível gerar o PDF: instale o Inkscape ou a biblioteca "
            "CairoSVG (pip install cairosvg)."
        ) from exc

    cairosvg.svg2pdf(
        url=str(svg_path),
        write_to=str(pdf_path),
    )


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
    pdf_output = out_dir / f"{base_name}.pdf"

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
        converter_svg_para_pdf(svg_output, pdf_output)
        print(f"PDF salvo em: {pdf_output}")

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
    exportar_diagramas_com_tonto_view(
                    input_path="../src/bases/despesas/base-despesas.tonto",
                    output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
                    output_name="base-despesas-conceitos-centrais",
                    view_file="../src/bases/despesas/views/versoes_da_view/base-despesas-conceitos-centrais.tontoview"
        )
    exportar_diagramas_com_tonto_view(
                        input_path="../src/bases/despesas/base-despesas.tonto",
                        output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
                        output_name="base-despesas-tipos-de-registro",
                        view_file="../src/bases/despesas/views/versoes_da_view/base-despesas-tipos-de-registro.tontoview"
            )
    exportar_diagramas_com_tonto_view(
                        input_path="../src/bases/despesas/base-despesas.tonto",
                        output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
                        output_name="base-despesas-classificadores",
                        view_file="../src/bases/despesas/views/versoes_da_view/base-despesas-classificadores.tontoview"
            )

def exportarDiagramas():
    exportarNucleo()
    exportarReceitas()
    exportarDespesas()

def _escapar_turtle_string(texto: str) -> str:
    """Escapa aspas e quebras de linha para literais Turtle seguros."""
    if not texto:
        return ""
    return (
        texto.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )

def exportar_ontologias_operacionais(
    src_dir: str = "../src",
    output_dir: str = "./ttl",
    tonto_json_path: str = "../tonto.json"
):
    """
    Lê tonto.json, exporta exclusivamente os arquivos .tonto listados em 'packages'
    e posiciona o cabeçalho owl:Ontology com todos os metadados do módulo logo após os prefixos.
    """
    root_path = Path(src_dir).resolve()
    out_dir_path = Path(output_dir).resolve()
    json_path = Path(tonto_json_path).resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"Diretório de origem não encontrado: {root_path}")
    if not json_path.exists():
        raise FileNotFoundError(f"Arquivo tonto.json não encontrado: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        config_tonto: Dict[str, Any] = json.load(f)

    packages: Dict[str, Dict[str, Any]] = config_tonto.get("packages", {})
    ontology_name = config_tonto.get("ontologyName", "Ontologia do Portal da Transparência do ES")
    ontology_acronym = config_tonto.get("ontologyAcronym", "OPTES")
    authors: list[str] = config_tonto.get("authors", [])

    if not packages:
        print("Nenhum módulo encontrado em 'packages' no tonto.json.")
        return

    out_dir_path.mkdir(parents=True, exist_ok=True)

    todos_tonto_files = list(root_path.glob("**/*.tonto"))
    tonto_files_filtrados = [f for f in todos_tonto_files if f.stem in packages]

    if not tonto_files_filtrados:
        print(f"Nenhum arquivo .tonto correspondente aos pacotes {list(packages.keys())} encontrado em: {root_path}")
        return

    try:
        print(f"Exportando {len(tonto_files_filtrados)} módulos definidos em packages: {[f.stem for f in tonto_files_filtrados]}")

        paths_str = [str(f) for f in tonto_files_filtrados]
        cmd_parts = ["npx", "tonto", "gufo"] + paths_str + [f"--out-dir={str(out_dir_path)}"]
        cmd_str = " ".join([f'"{p}"' if " " in p else p for p in cmd_parts])

        subprocess.run(cmd_str, shell=True, check=True, text=True)

        # Pós-processamento: reconstrói o cabeçalho owl:Ontology logo após os prefixos
        for modulo_key, dados_modulo in packages.items():
            ttl_file = out_dir_path / f"{modulo_key}.ttl"
            if not ttl_file.exists():
                print(f"Aviso: Arquivo esperado {ttl_file.name} não foi gerado.")
                continue

            g = rdflib.Graph()
            g.parse(str(ttl_file), format="turtle")

            # Garante os namespaces necessários no grafo
            g.bind("dcterms", DCTERMS)
            g.bind("vann", VANN)
            g.bind("owl", OWL)
            g.bind("rdfs", RDFS)

            # Recupera a URI da ontologia e os owl:imports existentes (ex: gufo:, nucleo:, etc.)
            ontologias = list(g.subjects(RDF.type, OWL.Ontology))
            if ontologias:
                ont_uri = ontologias[0]
                ont_uri_str = str(ont_uri)
                imports_existentes = list(g.objects(ont_uri, OWL.imports))
                # Remove o bloco owl:Ontology antigo do grafo para não duplicar no corpo
                g.remove((ont_uri, None, None))
            else:
                ont_uri_str = f"https://example.org/ontologia-portal-transparencia-es/{modulo_key}"
                imports_existentes = [rdflib.URIRef("http://purl.org/nemo/gufo#")]

            # Serializa o restante do grafo sem o bloco owl:Ontology
            ttl_sem_cabecalho = g.serialize(format="turtle")

            # Separa as linhas de @prefix do restante das triplas
            linhas = ttl_sem_cabecalho.splitlines()
            linhas_prefixos = []
            linhas_corpo = []
            for linha in linhas:
                if linha.strip().startswith("@prefix") or linha.strip().startswith("PREFIX"):
                    linhas_prefixos.append(linha)
                else:
                    linhas_corpo.append(linha)

            # Garante que os prefixos dcterms: e vann: estejam declarados no topo
            texto_prefixos = "\n".join(linhas_prefixos)
            if "dcterms:" not in texto_prefixos:
                linhas_prefixos.append("@prefix dcterms: <http://purl.org/dc/terms/> .")
            if "vann:" not in texto_prefixos:
                linhas_prefixos.append("@prefix vann: <http://purl.org/vocab/vann/> .")

            # Prepara os dados específicos deste módulo
            module_desc = _escapar_turtle_string(dados_modulo.get("moduleDescription", ""))
            module_authors = dados_modulo.get("authors", authors)

            module_name = dados_modulo.get("moduleName", modulo_key)
            label_modulo = _escapar_turtle_string(f"{ontology_acronym}:{module_name}")
            titulo_completo = _escapar_turtle_string(
                f"{ontology_name} ({ontology_acronym}) - Módulo {module_name}"
            )

            # Prefixo preferencial sem hífen para seguir convenção Turtle (ex: base-receitas -> basereceitas ou conforme o .ttl)
            pref_prefix = modulo_key.replace("-", "")
            for pfx, ns in g.namespaces():
                if str(ns).rstrip("#/") == ont_uri_str.rstrip("#/") and pfx:
                    pref_prefix = pfx
                    break

            pref_uri = ont_uri_str if ont_uri_str.endswith(("#", "/")) else f"{ont_uri_str}#"

            # Formata os autores
            autores_formatados = ",\n        ".join(
                f'"{_escapar_turtle_string(a)}"' for a in module_authors
            )

            # Formata os owl:imports preservando gufo: e eventuais imports de outros módulos
            imports_formatados_lista = []
            for imp in imports_existentes:
                imp_str = str(imp)
                if imp_str == "http://purl.org/nemo/gufo#":
                    imports_formatados_lista.append("gufo:")
                else:
                    imports_formatados_lista.append(f"<{imp_str}>")
            if not imports_formatados_lista:
                imports_formatados_lista.append("gufo:")
            imports_str = ", ".join(imports_formatados_lista)

            # Monta o bloco owl:Ontology exatamente no padrão solicitado
            bloco_ontologia = f"""<{ont_uri_str}> a owl:Ontology ;
    rdfs:label "{label_modulo}"@pt-br ;
    dcterms:creator {autores_formatados} ;
    dcterms:description "{module_desc}"@pt-br ;
    dcterms:title "{titulo_completo}"@pt-br ;
    vann:preferredNamespacePrefix "{pref_prefix}" ;
    vann:preferredNamespaceUri "{pref_uri}" ;
    rdfs:comment "{module_desc}"@pt-br ;
    owl:imports {imports_str} ."""

            # Junta prefixos + bloco owl:Ontology + restante das triplas
            corpo_limpo = "\n".join(linhas_corpo).lstrip("\n")
            conteudo_final = (
                "\n".join(linhas_prefixos)
                + "\n\n"
                + bloco_ontologia
                + "\n\n"
                + corpo_limpo
                + "\n"
            )

            with open(ttl_file, "w", encoding="utf-8") as f_out:
                f_out.write(conteudo_final)

            print(f"Metadados e descrição posicionados após os prefixos em: {ttl_file.name}")

        print(f"Ontologias operacionais exportadas com sucesso para: {out_dir_path}")

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
    linha = f"\\seqsplit{{{label_str}}} &\n{comment_str} \n\\\\ \\hline\n"
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
    exportarDiagramas()
    exportar_ontologias_operacionais()
    gerar_dicionarios()
    