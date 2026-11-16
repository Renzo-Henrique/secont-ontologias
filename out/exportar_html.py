import subprocess
from pathlib import Path
import re
import rdflib
from rdflib.namespace import RDF, OWL, RDFS, DCTERMS

def converter_latex_para_html(texto: str) -> str:
    """
    Função auxiliar para substituir 
    padrões textit{} por tags HTML de itálico (<em>...</em>).
    """
    if not texto:
        return ""
    
    # 1. Substitui qualquer  '\t' por vazio
    texto_sem_barra = texto.replace("\t", "")
    
    # 2. Verifica o padrão textit{...} (já sem a barra) e substitui o conteúdo por <em>...</em>
    return re.sub(r'extit\{([^}]*)\}', r'<em>\1</em>', texto_sem_barra)

def tratar_propriedades_inversas(g: rdflib.Graph) -> rdflib.Graph:
    """
    Varre o grafo em busca de restrições com owl:inverseOf anônimas e as converte 
    em propriedades nomeadas na mesma namespace, gerando o rótulo padrão 'inverseOf(...)'.
    """
    for restriction in list(g.subjects(RDF.type, OWL.Restriction)):
        on_property_nodes = list(g.objects(restriction, OWL.onProperty))
        if on_property_nodes:
            prop_node = on_property_nodes[0]
            # Verifica se a propriedade é um nó anônimo contendo owl:inverseOf
            inverse_of_nodes = list(g.objects(prop_node, OWL.inverseOf))
            if inverse_of_nodes:
                target_prop = inverse_of_nodes[0]
                
                # Extrai a namespace e o nome local da propriedade alvo de forma genérica
                target_str = str(target_prop)
                if "#" in target_str:
                    ns, target_name = target_str.rsplit("#", 1)
                    ns_uri = rdflib.Namespace(ns + "#")
                else:
                    ns, target_name = target_str.rsplit("/", 1)
                    ns_uri = rdflib.Namespace(ns + "/")

                # Define o nome local e a URI da nova propriedade inversa nomeada
                inv_local_name = f"inverseOf_{target_name.replace('.', '_')}"
                inv_prop_uri = ns_uri[inv_local_name]

                # Adiciona a propriedade inversa nomeada ao grafo com o label formatado
                g.add((inv_prop_uri, RDF.type, OWL.ObjectProperty))
                g.add((inv_prop_uri, OWL.inverseOf, target_prop))
                g.add((inv_prop_uri, RDFS.label, rdflib.Literal(f"inverseOf({target_name})", lang="pt-br")))

                # Substitui a referência anônima antiga pela nova propriedade nomeada na restrição
                g.remove((restriction, OWL.onProperty, prop_node))
                g.add((restriction, OWL.onProperty, inv_prop_uri))

    return g

def gerar_documentacao_html(
    nome_ontologia: str,
    sigla_ontologia: str,
    proposito_ontologia: str,
    ttl_dir: str = "./ttl", 
    output_docs_dir: str = "./html"
):
    """
    Detecta arquivos .ttl, trata propriedades inversas, injeta metadados necessários 
    para o pyLODE, gera a documentação HTML individual e cria o index.html em ordem reversa.
    """
    if not nome_ontologia or not sigla_ontologia or not proposito_ontologia:
        raise ValueError(
            "Erro: Os argumentos 'nome_ontologia', 'sigla_ontologia' e 'proposito_ontologia' são obrigatórios!"
        )

    ttl_path = Path(ttl_dir).resolve()
    docs_path = Path(output_docs_dir).resolve()

    if not ttl_path.exists():
        print(f"Diretório de ontologias TTL não encontrado: {ttl_path}")
        return

    docs_path.mkdir(parents=True, exist_ok=True)

    ttl_files = list(ttl_path.glob("*.ttl"))

    if not ttl_files:
        print(f"Nenhum arquivo .ttl encontrado em: {ttl_path}")
        return

    modulos_gerados = []

    print(f"Encontrados {len(ttl_files)} arquivos .ttl. Processando e gerando documentação HTML com pyLODE...")

    for ttl_file in ttl_files:
        nome_modulo = ttl_file.stem
        arquivo_html_saida = docs_path / f"{nome_modulo}.html"
        
        try:
            g = rdflib.Graph()
            g.parse(str(ttl_file), format="turtle")

            # 1. Trata propriedades inversas anônimas gerando referências limpas
            g = tratar_propriedades_inversas(g)

            # 2. Identifica a URI principal da ontologia e injeta metadados se necessário
            ontologias = list(g.subjects(RDF.type, OWL.Ontology))
            if ontologias:
                ont_uri = ontologias[0]
                if not list(g.objects(ont_uri, RDFS.label)) and not list(g.objects(ont_uri, DCTERMS.title)):
                    g.add((ont_uri, RDFS.label, rdflib.Literal(f"{nome_ontologia} - Módulo {nome_modulo}", lang="pt-br")))
                if not list(g.objects(ont_uri, RDFS.comment)) and not list(g.objects(ont_uri, DCTERMS.description)):
                    g.add((ont_uri, RDFS.comment, rdflib.Literal(proposito_ontologia, lang="pt-br")))
            
            # Salva o TTL temporário tratado
            ttl_temporario = docs_path / f"_temp_{ttl_file.name}"
            g.serialize(destination=str(ttl_temporario), format="turtle")
            
            cmd = ["pylode", str(ttl_temporario), "-o", str(arquivo_html_saida)]
            subprocess.run(cmd, check=True, text=True)
            
            if ttl_temporario.exists():
                ttl_temporario.unlink()

            print(f"Documentação gerada para o módulo: {nome_modulo} -> {arquivo_html_saida}")
            modulos_gerados.append(nome_modulo)

        except subprocess.CalledProcessError as e:
            print(f"Erro ao gerar documentação pyLODE para {ttl_file.name}: {e}")
        except FileNotFoundError:
            print("Erro: O comando 'pylode' não foi encontrado. Certifique-se de instalar com 'pip install pylode'.")
            return

    proposito_html = converter_latex_para_html(proposito_ontologia)
    index_html_path = docs_path / "index.html"
    
    # Gera a listagem dos módulos em ordem reversa (reverse-order)
    itens_lista_html = "\n".join(
        f'        <li><a href="{mod}.html">Módulo <strong>{mod}</strong></a></li>' for mod in sorted(modulos_gerados, reverse=True)
    )

    conteudo_index = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentação - {nome_ontologia} ({sigla_ontologia})</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px auto;
            max-width: 800px;
            padding: 0 20px;
            color: #333;
        }}
        h1 {{
            color: #0056b3;
        }}
        .badge {{
            background-color: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #495057;
        }}
        ul {{
            margin-top: 20px;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>{nome_ontologia} <span class="badge">{sigla_ontologia}</span></h1>
    <p><strong>Propósito:</strong> {proposito_html}</p>
    <p>Esta ontologia está estruturada em módulos para melhor organização e reutilização de conceitos. Abaixo estão disponíveis os links para acessar a documentação detalhada de cada módulo específico gerada via pyLODE:</p>
    <ul>
{itens_lista_html}
    </ul>
</body>
</html>
"""

    with open(index_html_path, "w", encoding="utf-8") as f_index:
        f_index.write(conteudo_index)

    print(f"Página principal gerada com sucesso em: {index_html_path}")



_nome_ontologia = """Ontologia do Portal da Transparência do ES"""
_sigla_ontologia = """OPTES"""
_proposito_ontologia = """O propósito da ontologia é representar os conceitos relacionados aos dados publicados no Portal da Transparência do Poder Executivo do Estado do Espírito Santo e os conceitos que são necessários à interpretação dessas informações (\textit{what}); de modo a estabelecer uma conceituação explícita e compartilhada que apoie a compreensão das bases por usuários humanos, a integração semântica entre diferentes conjuntos de dados e a posterior representação dos dados por meio de tecnologias da Web Semântica (\textit{for what}); visando reduzir ambiguidades na interpretação dos dados, favorecer sua interoperabilidade semântica com dados internos e externos e ampliar as possibilidades de integração, consulta e reutilização automatizada das informações publicadas (\textit{why})."""

if __name__ == "__main__":
    gerar_documentacao_html(
        nome_ontologia=_nome_ontologia,
        sigla_ontologia=_sigla_ontologia,
        proposito_ontologia=converter_latex_para_html(_proposito_ontologia)
    )