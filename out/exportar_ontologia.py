import os
import subprocess
from pathlib import Path
from typing import Optional

_PREFIX_OUTPUT_DIR = "./diagramas"
_PREFIX_NUCLEO = "/nucleo"
_PREFIX_RECEITAS = "/receitas"
_PREFIX_DESPESAS = "/despesas"


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
            output_name="base-receitas_atributos",
            view_file="../src/bases/receitas/views/versoes_da_view/base-receitas_COM_atributos.tontoview"
        )

def exportarDespesas():
    exportar_diagramas_com_tonto_view(
            input_path="../src/bases/despesas/base-despesas.tonto",
            output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
            view_file="../src/bases/despesas/views/base-despesas.tontoview"
    )
    exportar_diagramas_com_tonto_view(
            input_path="../src/bases/despesas/base-despesas-orcamentos-despesa.tonto",
            output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
            view_file="../src/bases/despesas/views/base-despesas-orcamentos-despesa.tontoview"
    )
    exportar_diagramas_com_tonto_view(
            input_path="../src/bases/despesas/base-despesas-orcamentos-execucoes.tonto",
            output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
            view_file="../src/bases/despesas/views/base-despesas-orcamentos-execucoes.tontoview"
    )
    exportar_diagramas_com_tonto_view(
            input_path="../src/bases/despesas/base-despesas-restos-a-pagar.tonto",
            output_dir=_PREFIX_OUTPUT_DIR+_PREFIX_DESPESAS,
            view_file="../src/bases/despesas/views/base-despesas-restos-a-pagar.tontoview"
    )
    
# Exemplo de uso:
if __name__ == "__main__":
    exportarNucleo()
    exportarReceitas()
    exportarDespesas()
    