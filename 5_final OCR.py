import cv2
import numpy as np
import pandas as pd
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

json_path = BASE_DIR / "outcome" / "coordenadas.json"

with open(json_path, "r", encoding="utf-8") as f:
    coordenadas = json.load(f)

# Converter de volta para tupla (opcional)
coordenadas = {k: tuple(v) for k, v in coordenadas.items()}

# --------------- ENDEREÇO PASTA COM IMAGENS ALINHADAS ---------------

SUBPASTA = ""
# caso os formulários sejam segmentados em subpastas com identificação de grupos tais como: salas de aula, escolas, regiões, idades etc
# nessa caso, aplicar \\{SUBPASTA} ao final do path da pasta principal para garantir essa categoria no banco de dados final
# exemplo abaixo:
# PASTA = (fr"C:\Users\morei\Documents\Workspace\Ocerizacao\paginas_jpg_alinhadas\\{SUBPASTA}")


PASTA = BASE_DIR / "data" / "mock_data_aligned_jpg"

# ----- FUNÇÃO PARA AVALIAR PIXELS ESCUROS NO ESPAÇO DA ALTERNATIVA -----

def verificar_marcacao(img, x, y, w, h, thresh=200, minimo_pixels_escuros=200):
    """
    Retorna:
      - marcada (True/False)
      - quantidade de pixels escuros
    """
    roi = img[y:y+h, x:x+w]

    pixels_escuros = np.sum(roi < thresh)
    marcada = pixels_escuros > minimo_pixels_escuros

    return bool(marcada), int(pixels_escuros)

## variáveis "thresh" e "minimo_pixels_escuros" podem ser alterados para tornar a identificação
## mais ou meno sensivel


# ----- FUNÇÃO APLICAR AVALIAÇÃO À TODAS AS ALTERNATIVAS DA PÁGINA -----

def verificar_questionario(img, coordenadas):
    resultados = {}

    for alternativa, (x, y, w, h) in coordenadas.items():
        marcada, qtd = verificar_marcacao(img, x, y, w, h)

        resultados[alternativa] = {
            "marcada": marcada,
            "pixels_escuros": qtd
        }

    return resultados


# --------------- PROCESSAR TODAS AS IMAGENS DE UMA PASTA ---------------

def processar_pasta(pasta_imagens, coordenadas, arquivo_saida):
    linhas_csv = []
    extensoes_validas = (".jpg", ".jpeg", ".png", ".tif", ".bmp")

    arquivos = sorted([f for f in os.listdir(pasta_imagens) if f.lower().endswith(extensoes_validas)])

    if not arquivos:
        print("❌ Nenhuma imagem encontrada na pasta.")
        return

    for i, nome_img in enumerate(arquivos, start=1):
        caminho = os.path.join(pasta_imagens, nome_img)
        print(f"🔍 Processando página {i}: {nome_img}")

        img = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"⚠ Erro ao abrir: {nome_img}")
            continue

        resultados = verificar_questionario(img, coordenadas)

        # 🔥 formato solicitado: tudo em sequência, com número da página
        for alternativa, info in resultados.items():
            marcada_01 = 1 if info["marcada"] else 0
            
            linhas_csv.append({
                "sala": SUBPASTA,
                "pagina": i,
                "alternativa": alternativa,
                "marcada": marcada_01,
                "pixels_escuros": info["pixels_escuros"]
            })

    # ---------- salvar CSV ----------
    df = pd.DataFrame(linhas_csv)
    df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"\n✅ Arquivo salvo: {arquivo_saida}")
    return df


# --------------- EXECUÇÃO ---------------
arquivo_saida = BASE_DIR / "outcome" / f"resultado_final_{SUBPASTA}.csv"
df = processar_pasta(PASTA, coordenadas, arquivo_saida)


