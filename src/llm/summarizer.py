import os
# importa o LocalLLM que está lá no model.py
from .model import LocalLLM

class Summarizer:
    def __init__(self):
        # conecta com o modelo
        self.llm = LocalLLM()

    def make_summary(self, text):
        """
        Recebe o texto do PDF e pede para o modelo resumir.
        """
        return self.llm.summarize(text)

def save_to_file(content, original_filename):
    """
    Salva o resumo em um arquivo txt com o mesmo nome do pdf
    """
    base_name = os.path.splitext(original_filename)[0]
    output_filename = f"{base_name}_resumo.txt"
    
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(content)
        return output_filename
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return None