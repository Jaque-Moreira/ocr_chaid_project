from pdf2image import convert_from_path
import os

pdf_path = r"C:\\Users\\morei\\OneDrive\\Documentos\\Workspace\\Ocerizacao\\mock_data_forms.pdf"

output_folder = r"C:\\Users\\morei\\OneDrive\\Documentos\\Workspace\\Ocerizacao\\mock_data_forms_jpg"

# Garante que a pasta existe
os.makedirs(output_folder, exist_ok=True)

# Converte todas as páginas
pages = convert_from_path(pdf_path, dpi=400)

# Salva cada página como JPG
for i, page in enumerate(pages, start=1):
    if i <10:
        output_path = os.path.join(output_folder, f"page_0{i}.jpg")
        page.save(output_path, "JPEG")
        print(f"✅ Página {i} salva em: {output_path}")
    else:
        output_path = os.path.join(output_folder, f"page_{i}.jpg")
        page.save(output_path, "JPEG")
        print(f"✅ Página {i} salva em: {output_path}")
    
