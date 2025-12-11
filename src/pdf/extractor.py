import os
import fitz  # PyMuPDF
import re
from collections import Counter
from nltk.corpus import stopwords
import string

def extract_text_from_pdf(pdf_path):
    """
    Função simples para abrir o PDF e retornar todo o texto como uma string.
    """
    if not os.path.exists(pdf_path):
        return ""

    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"
        doc.close()
        return full_text
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
        return ""

class PDFAnalyzer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        # tenta carregar stopwords, baixa se não tiver
        try:
            self.stop_words = set(stopwords.words('portuguese'))
        except LookupError:
            import nltk
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('portuguese'))

    def analyze(self):
        """
        Executa a análise completa e retorna um dicionário com os metadados.
        """
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {self.pdf_path}")

        # tamanho do arquivo
        file_size_bytes = os.path.getsize(self.pdf_path)

        # abre o PDF
        doc = fitz.open(self.pdf_path)
        
        # número total de páginas
        num_pages = len(doc)
        
        full_text = ""
        for page in doc:
            full_text += page.get_text() + " "

        doc.close()

        # Processamento de texto para contagens
        words = self._process_text(full_text)
        
        # número total de palavras
        total_words = len(words)

        # filtrar stopwords e palavras muito curtas
        cleaned_words = [
            w for w in words 
            if w not in self.stop_words and len(w) > 1 and not w.isdigit()
        ]

        # tamanho do vocabulário (palavras únicas)
        vocab_size = len(set(cleaned_words))

        # top 10 palavras mais comuns
        word_counts = Counter(cleaned_words)
        top_10 = word_counts.most_common(10)

        return {
            "num_pages": num_pages,
            "total_words": total_words,
            "file_size_bytes": file_size_bytes,
            "vocab_size": vocab_size,
            "top_10_words": top_10
        }

    def _process_text(self, text):
        """
        Limpa o texto, remove pontuação e retorna lista de tokens.
        """
        text = text.lower()
        
        tokens = re.findall(r'\b[a-záàâãéèêíïóôõöúçñ]+\b', text)
        
        return tokens