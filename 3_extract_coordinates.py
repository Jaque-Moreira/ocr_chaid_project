import json
import cv2
from pathlib import Path

# === CONFIGURAÇÃO ===

BASE_DIR = Path(__file__).resolve().parent

IMAGEM_PATH = BASE_DIR / "data" / "mock_data_forms_jpg"/"page_01.jpg" # pode ser .png ou extraída do PDF
ESCALA = 0.20  # redimensiona visualização (não altera coordenadas reais)

# === LISTAS GLOBAIS ===
pontos_display = []   # coordenadas na imagem redimensionada
pontos_originais = [] # coordenadas convertidas para escala real

# === FUNÇÕES ===
def mostrar_coordenadas(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Coordenada na imagem exibida
        pontos_display.append((x, y))
        
        # Conversão para escala original
        x_orig = int(x / ESCALA)
        y_orig = int(y / ESCALA)
        pontos_originais.append((x_orig, y_orig))
        
        print(f"Clique: display=({x}, {y}) | original=({x_orig}, {y_orig})")
        
        # Feedback visual (Desenha um pequeno círculo onde clicou)
        cv2.circle(img_display, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Clique para medir", img_display)

# === CARREGA IMAGEM ===
img = cv2.imread(IMAGEM_PATH)
h, w = img.shape[:2]
img_display = cv2.resize(img, (int(w * ESCALA), int(h * ESCALA)))
pontos = []

print("🖱️ Clique nos pontos desejados (parênteses das alternativas).")
print("Pressione ESC para encerrar.")

cv2.imshow("Clique para medir", img_display)
cv2.setMouseCallback("Clique para medir", mostrar_coordenadas)

# Loop até apertar ESC
while True:
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

# === RESULTADO FINAL ===
print("\n--- Coordenadas finais (escala original) ---")
for i, (x, y) in enumerate(pontos_originais, start=1):
    print(f"{i}: (x={x}, y={y})")

print("\nLista pronta para uso no OCR:")
print(pontos_originais)


# ==============================
# ENTRADAS DO USUÁRIO
# ==============================

# Vetor de identificação das alternativas (alterar de acordo com o necessário)
identificadores = [
    "1a","1b","1c","1d","1e","1f","1g",
    "2a","2b","2c","2d","2e","2f",
    "3a","3b","3c",
    "4a","4b","4c","4d","4e","4f",
    "6a","6b"
]

# Dimensões da caixa delimitadora (alterar de acordo com o necessário)
largura = 57
altura = 45

# ==============================
# CONSTRUÇÃO DO DICIONÁRIO
# ==============================

coordenadas = {}

for id_alt, (x, y) in zip(identificadores, pontos_originais):
    coordenadas[id_alt] = (x, y, largura, altura)

print("Dicionário de coordenadas OCR:\n")
for k, v in coordenadas.items():
    print(f'"{k}": {v}')
    

# ==========================
# SALVAR JSON
# ==========================

# JSON não suporta tuplas → converter para lista
coordenadas_json = {k: list(v) for k, v in coordenadas.items()}

json_path = BASE_DIR / "outcome" / "coordenadas.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(coordenadas_json, f, indent=4, ensure_ascii=False)
print(f"\n✅ JSON salvo com sucesso em:\n{json_path}")











