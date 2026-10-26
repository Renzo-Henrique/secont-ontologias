from pathlib import Path
import os
import shutil

def converter_svgs():
    # Cria o subdiretório de destino se não existir
    output_dir = Path("exportados")
    output_dir.mkdir(exist_ok=True)
    
    # Verifica se o Inkscape está disponível no sistema
    inkscape_path = shutil.which("inkscape")
    if not inkscape_path:
        print("❌ Erro: O Inkscape não foi encontrado no PATH do sistema.")
        print("Por favor, certifique-se de que o Inkscape está instalado e acessível pelo terminal.")
        return

    # Busca todos os arquivos .svg no diretório atual
    svg_files = list(Path(".").glob("*.svg"))
    
    if not svg_files:
        print("Nenhum arquivo .svg encontrado no diretório atual.")
        return

    print(f"Encontrados {len(svg_files)} arquivo(s) .svg. Iniciando conversão via Inkscape...\n")

    for svg_path in svg_files:
        base_name = svg_path.stem  # Nome do arquivo sem a extensão
        
        pdf_out = output_dir / f"{base_name}.pdf"
        png_out = output_dir / f"{base_name}.png"
        
        print(f"Processando: {svg_path.name} -> Pasta '{output_dir}'")
        
        # Converte para PDF mantendo vetores e legendas nítidas (usando os.system)
        cmd_pdf = f'"{inkscape_path}" "{svg_path}" --export-type=pdf --export-filename="{pdf_out}"'
        os.system(cmd_pdf)
        
        # Converte para PNG em alta qualidade (300 DPI)
        cmd_png = f'"{inkscape_path}" "{svg_path}" --export-type=png --export-filename="{png_out}" --export-dpi=300'
        os.system(cmd_png)

    print(f"\n✨ Conversão concluída! Todos os arquivos foram salvos na pasta '{output_dir}' com perfeição.")

if __name__ == "__main__":
    converter_svgs()