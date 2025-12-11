import os
import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path, output_base_dir="imagens"):
    """
    Extrai imagens do PDF e salva no diretório organizado.
    Retorna uma LISTA com os caminhos das imagens salvas.
    """
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo {pdf_path} não encontrado.")
        return []  # Retorna lista vazia em caso de erro

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Erro ao abrir PDF: {e}")
        return []

    # pega o nome do arquivo sem extensão para criar a pasta
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    output_dir = os.path.join(output_base_dir, pdf_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Iniciando extração de imagens para: {output_dir} ---")
    
    saved_images_list = []
    
    # itera sobre cada página
    for page_index, page in enumerate(doc):
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]

            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"pag{page_index+1}_img{img_index+1}.{image_ext}"
                image_path = os.path.join(output_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                saved_images_list.append(image_path)
                
            except Exception as e:
                print(f"Erro ao extrair imagem da página {page_index+1}: {e}")
            
    doc.close()
    
    print(f"Concluído: {len(saved_images_list)} imagens extraídas.")
    
    return saved_images_list