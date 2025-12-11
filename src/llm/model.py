import torch
from transformers import pipeline

class LocalLLM:
    def __init__(self):
        print("Carregando modelo Qwen...")
        self.model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        
        try:
            self.pipe = pipeline(
                "text-generation",
                model=self.model_id,
                device_map="auto",
                dtype=torch.float32,
                max_new_tokens=1000, # limite de saída (tamanho do resumo)
            )
            print("Modelo Qwen carregado com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.pipe = None

    def summarize(self, text):
        if not self.pipe:
            return "Modelo não disponível."

        # cria o prompt instruindo o modelo
        messages = [
            {"role": "system", "content": "Você é um assistente útil que resume textos técnicos em português."},
            {"role": "user", "content": f"Resuma o seguinte texto:\n\n{text}"}
        ]
        
        try:
            # o parâmetro max_new_tokens controla o tamanho da resposta gerada
            output = self.pipe(messages, max_new_tokens=1000)
            generated_content = output[0]['generated_text'][-1]['content']
            return generated_content
        except Exception as e:
            return f"Erro na geração: {e}"