Este projeto é uma ferramenta em Python que processa arquivos PDF para extrair informações estatísticas, imagens e gerar resumos automáticos utilizando Inteligência Artificial (LLM Local - Qwen).

## Funcionalidades

1.  **Análise Estatística**: Contagem de páginas, palavras totais, tamanho do vocabulário e identificação das palavras mais frequentes.
2.  **Extração de Imagens**: Identifica e extrai todas as imagens contidas no PDF, salvando-as em uma pasta organizada.
3.  **Resumo com IA**: Utiliza um modelo de linguagem local (Qwen) para ler o texto do PDF e gerar um resumo conciso.

## Instalação e Dependências

Para que o projeto funcione, você precisa instalar as bibliotecas listadas no arquivo `requirements.txt`. Siga os passos abaixo:

### 1. Pré-requisitos
Certifique-se de ter o **Python** (versão 3.9 ou superior) instalado na sua máquina.

### 2. Configurando o Ambiente
É recomendado criar um ambiente virtual para não misturar as bibliotecas do projeto com as do seu sistema.

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**No Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```
Com o ambiente ativo, rode no seu terminal: `pip install -r requirements.txt`

Na raiz do repositório, execute: `python main.py <caminho_do_seu_arquivo.pdf>`

Exemplo atual: `python main.py RomaAntigapdf.pdf`

