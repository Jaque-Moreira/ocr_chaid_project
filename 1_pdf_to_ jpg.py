from pdf2image import convert_from_path
from pathlib import Path
import os

# ==========================
# CONFIGURAÇÕES DE PATH
# ==========================


BASE_DIR = Path(__file__).resolve().parent

pdf_path = BASE_DIR / "data" / "mock_data_forms.pdf"
output_folder = BASE_DIR / "data" / "mock_data_forms_jpg"

# ==========================
# VALIDAÇÕES
# ==========================

if not pdf_path.exists():
    raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

os.makedirs(output_folder, exist_ok=True)

# ==========================
# CONVERSÃO PDF → JPG
# ==========================

pages = convert_from_path(
    pdf_path,
    dpi=400
)

for i, page in enumerate(pages, start=1):
    nome = f"page_{i:02d}.jpg"   # page_01.jpg, page_02.jpg ...
    output_path = output_folder / nome
    page.save(output_path, "JPEG")
    print(f"✅ Página {i} salva em: {output_path}")
