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
                    # Suporta formato antigo (item com "url") e novo (item com "parts")
                    if isinstance(item, dict):
                        if "url" in item:
                            processados.add(item["url"])
                        elif "parts" in item and isinstance(item["parts"], list):
                            for part in item["parts"]:
                                if isinstance(part, dict) and "url" in part:
                                    processados.add(part["url"])
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

            for entrada in os.listdir(autor_path):
                entrada_path = os.path.join(autor_path, entrada)

                # Caso 1: arquivo diretamente dentro do autor (comportamento existente)
                if os.path.isfile(entrada_path):
                    url = f"{BASE_URL}/{categoria}/{autor}/{entrada}"
                    if url not in processados:
                        novos.append({
                            "url": url,
                            "categoria": categoria,
                            "autor": autor
                        })

                # Caso 2: existe uma pasta dentro do autor → agrupar em parts
                elif os.path.isdir(entrada_path):
                    parts = []
                    for nome_arquivo in sorted(os.listdir(entrada_path)):
                        caminho_arquivo = os.path.join(entrada_path, nome_arquivo)
                        if os.path.isfile(caminho_arquivo):
                            part_url = f"{BASE_URL}/{categoria}/{autor}/{entrada}/{nome_arquivo}"
                            parts.append({"url": part_url})

                    # Apenas adiciona se houver pelo menos um arquivo
                    if parts:
                        # Se todos já foram processados, não adiciona
                        if not all(part["url"] in processados for part in parts):
                            novos.append({
                                # categoria passa a ser o nome da subpasta (ex.: "3d")
                                "categoria": entrada,
                                "autor": autor,
                                "parts": parts
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