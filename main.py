import sys
import os

from src.pdf.extractor import PDFAnalyzer, extract_text_from_pdf
from src.pdf.images import extract_images_from_pdf
from src.llm.summarizer import Summarizer, save_to_file

def main():
    # verifica argumentos
    if len(sys.argv) < 2:
        print("Uso correto: python main.py <caminho_do_pdf>")
        return

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo '{pdf_path}' nao encontrado.")
        return

    print(f"\nIniciando processamento: {pdf_path}")
    print("-" * 50)

    # PARTE 1: ANALISE ESTATISTICA
    print("Executando analise estatistica...")
    
    try:
        analyzer = PDFAnalyzer(pdf_path)
        results = analyzer.analyze()
        
        print("\n--- RELATORIO DE ANALISE ---")
        print(f"Total de paginas: {results['num_pages']}")
        print(f"Total de palavras: {results['total_words']}")
        print(f"Vocabulario (palavras unicas): {results['vocab_size']}")
        
        size_kb = results['file_size_bytes'] / 1024
        print(f"Tamanho do arquivo: {size_kb:.2f} KB")

        print("\nTop 10 palavras mais frequentes:")
        for word, count in results['top_10_words']:
            print(f" - {word}: {count}")
        print("-" * 50)

    except Exception as e:
        print(f"Erro ao analisar estatisticas: {e}")

    # PARTE 2: EXTRACAO DE IMAGENS
    print("\nVerificando imagens no documento...")
    
    try:
        # define uma pasta de saida baseada no nome do PDF para ficar organizado
        nome_arquivo = os.path.splitext(os.path.basename(pdf_path))[0]
        pasta_imagens = os.path.join("images", nome_arquivo)
        
        # cria a pasta se não existir
        os.makedirs(pasta_imagens, exist_ok=True)
        
        # chama a função de extração
        imagens_salvas = extract_images_from_pdf(pdf_path, pasta_imagens)
        
        if imagens_salvas:
            print(f"Sucesso! {len(imagens_salvas)} imagens extraidas.")
            print(f"Imagens salvas em: {os.path.abspath(pasta_imagens)}")
        else:
            print("Nenhuma imagem encontrada para extrair.")
            
    except Exception as e:
        print(f"Erro na extracao de imagens: {e}")

    print("-" * 50)

    # PARTE 3: RESUMO (LLM)
    print("\nIniciando geracao de resumo...")

    texto_completo = extract_text_from_pdf(pdf_path)
    
    if not texto_completo:
        print("Erro: Nao foi possivel extrair texto para o resumo.")
        return

    # corta o texto para nao estourar a memoria (10k caracteres)
    texto_para_resumir = texto_completo[:10000]
    
    try:
        resumidor = Summarizer()
        
        print("Gerando resumo (aguarde)...")
        resumo = resumidor.make_summary(texto_para_resumir)
        
        arquivo_saida = save_to_file(resumo, pdf_path)
        
        print("\n" + "="*50)
        print("PROCESSO CONCLUIDO")
        print("="*50)
        
        print(f"Resumo salvo em: {os.path.abspath(arquivo_saida)}")
        
        print("\n--- Previa do Resumo ---")
        print(resumo[:500] + "...")
        print("(veja o arquivo txt para o conteudo completo)")

    except Exception as e:
        print(f"Erro na geracao do resumo: {e}")

if __name__ == "__main__":
    main()