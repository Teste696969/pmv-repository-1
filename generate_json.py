import os
import json
import datetime
import glob

# Configurações
BASE_URL = "https://github.com/Teste696969/pmv-repository-1/raw/refs/heads/main"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Pasta onde o script está
OUTPUT_DIR = ROOT_DIR  # Onde salvar os JSONs

def carregar_processados():
    """Carrega todos os arquivos já processados dos JSONs anteriores"""
    processados = set()
    for file in glob.glob(os.path.join(OUTPUT_DIR, "json-*.json")):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for item in data:
                    processados.add(item["url"])
            except json.JSONDecodeError:
                pass  # ignora arquivos quebrados
    return processados

def gerar_json():
    processados = carregar_processados()
    novos = []

    for categoria in ["pmv"]:
        categoria_path = os.path.join(ROOT_DIR, categoria)
        if not os.path.isdir(categoria_path):
            continue

        for autor in os.listdir(categoria_path):
            autor_path = os.path.join(categoria_path, autor)
            if not os.path.isdir(autor_path):
                continue

            for arquivo in os.listdir(autor_path):
                arquivo_path = os.path.join(autor_path, arquivo)
                if os.path.isfile(arquivo_path):
                    url = f"{BASE_URL}/{categoria}/{autor}/{arquivo}"
                    if url not in processados:
                        novos.append({
                            "url": url,
                            "categoria": categoria,
                            "autor": autor
                        })

    if novos:
        # Nome do arquivo com data + hora (para sempre gerar um novo)
        data_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"json-{data_str}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(novos, f, indent=2, ensure_ascii=False)
        print(f"✅ Arquivo gerado: {output_file}")
        print(f"🔹 Total de novos adicionados: {len(novos)}")
    else:
        print("Nenhum item novo encontrado.")

if __name__ == "__main__":
    gerar_json()