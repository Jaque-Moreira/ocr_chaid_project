import cv2
import json
from pathlib import Path


with open("coordenadas_formulario.json", "r", encoding="utf-8") as f:
    coordenadas = json.load(f)

# Converter de volta para tupla (opcional)
coordenadas = {k: tuple(v) for k, v in coordenadas.items()}

# === CONFIGURAÇÕES ===
BASE_DIR = Path(__file__).resolve().parent

IMG_PATH = BASE_DIR / "data" / "mock_data_forms_jpg"/"page_01.jpg"

# === CARREGAR IMAGEM ===
img = cv2.imread(IMG_PATH)
if img is None:
    raise FileNotFoundError("Não foi possível carregar a imagem. Verifique o caminho em IMG_PATH.")

# === DESENHAR RETÂNGULOS ===
for alt, (x, y, w, h) in coordenadas.items():
    # Desenhar retângulo verde
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Adicionar texto (identificador)
    cv2.putText(img, f"{alt}", (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# === MOSTRAR IMAGEM ===
# cv2.imshow("Verificação das Caixas", img)
# print("✅ Caixas desenhadas. Pressione qualquer tecla na janela para fechar.")
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# === SALVA VERSÃO COM MARCAÇÕES ===

output_path = BASE_DIR / "outcome" / "visual_check_box.png"

cv2.imwrite(str(output_path), img)
print("💾 Imagem com marcações salva como 'visual_check_box.png'.")