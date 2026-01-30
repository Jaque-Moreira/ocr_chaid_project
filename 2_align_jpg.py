import cv2
import numpy as np
import os

# ---------------------------
# FUNÇÃO DE ALINHAMENTO (MESMA DO CÓDIGO ANTERIOR)
# ---------------------------
def alinhar_imagem(img, template):
    # Converte para grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # ORB detecta pontos-chave
    orb = cv2.ORB_create(5000)
    k1, d1 = orb.detectAndCompute(img_gray, None)
    k2, d2 = orb.detectAndCompute(temp_gray, None)

    # Matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(d1, d2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Pegamos os melhores 20% dos matches
    qtd = max(10, int(len(matches) * 0.2))  # evita zero matches
    matches = matches[:qtd]

    # Extraímos coordenadas
    pts1 = np.float32([k1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    pts2 = np.float32([k2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Calcula homografia
    H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC)

    # Warp para alinhar imagem ao template
    altura, largura = template.shape[:2]
    alinhada = cv2.warpPerspective(img, H, (largura, altura))

    return alinhada


# ---------------------------
# PROCESSAR TODAS AS IMAGENS DE UMA PASTA
# ---------------------------

template_path = r"C:\\Users\\morei\\Documents\\Workspace\\Ocerizacao\\paginas_jpg\\page_01.jpg"
input_folder = r"C:\\Users\\morei\\Documents\\Workspace\\Ocerizacao\\paginas_jpg\\911"
output_folder = r"C:\\Users\\morei\\Documents\\Workspace\\Ocerizacao\\paginas_jpg_alinhadas\\911"

# Garante que a pasta de saída exista
os.makedirs(output_folder, exist_ok=True)

# Carrega o template
template = cv2.imread(template_path)

# Extensões válidas
exts = (".jpg", ".jpeg", ".png")

print("🔎 Iniciando alinhamento das imagens...")

for filename in os.listdir(input_folder):
    if filename.lower().endswith(exts):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        print(f"➡ Alinhando: {filename}")

        # Alinha a imagem
        try:
            alinhada = alinhar_imagem(img, template)
        except Exception as e:
            print(f"⚠ Erro ao alinhar {filename}: {e}")
            continue

        # Caminho de saída
        out_path = os.path.join(output_folder, filename)

        # Salva imagem alinhada
        cv2.imwrite(out_path, alinhada)
        print(f"   ✔ Salvo: {out_path}")

print("\n🎉 Processo concluído! Todas as imagens foram alinhadas com sucesso.")



