Comparador de Respostas de Modelos de LLMs

Este projeto realiza a comparação de respostas geradas por diferentes modelos de Large Language Models (LLMs), incluindo Gemini, Mistral, Ollama (Mistral) e DeepSeek. A análise considera critérios como clareza, coerência, precisão da informação e criatividade.
Pré-requisitos

Antes de executar o projeto, certifique-se de que possui os seguintes requisitos instalados:

Python 3.10+

pip (gerenciador de pacotes do Python)

Ollama instalado e rodando localmente ou acessível remotamente

Instalação do Ollama

O Ollama precisa estar instalado na máquina local para que este projeto funcione corretamente. Para instalá-lo, siga as instruções abaixo conforme o seu sistema operacional:

Windows:

winget install Ollama.Ollama

macOS:

brew install ollama

Linux:

curl -fsSL https://ollama.com/install.sh | sh

Executando o Ollama

Após a instalação, inicie o Ollama executando o seguinte comando:

ollama serve &

Isso garantirá que ele esteja rodando localmente na porta 11434.

Caso prefira rodar o Ollama via Docker:
docker run -d -p 11434:11434 ollama/ollama

🚀 Funcionalidades

Obtém respostas de múltiplos modelos de LLMs.

Analisa as respostas com base em critérios linguísticos e semânticos.

Normaliza as pontuações entre 0 e 10.

Gera um ranking das respostas utilizando o Gemini.

🛠️ Tecnologias Utilizadas

Python

Google Gemini API

Mistral API

DeepSeek API

Ollama (Local LLM Serving)

LanguageTool (Correção gramatical)

NumPy (Normalização de dados)

📁 pythonProject
│-- config.py            # Configuração das chaves de API
│-- llm_compare.py       # Funções para obter respostas e analisá-las
│-- rank_compare.py      # Ranking das respostas com o Gemini
│-- main.py              # Arquivo principal para execução
│-- .env                 # Arquivo para armazenar as chaves de API

🔧 Configuração

1️⃣ Clonar o repositório

git clone git@github.com:karolyne04/desafio-cognitiva.git


2️⃣ Criar um ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

3️⃣ Instalar dependências

pip install -r requirements.txt

4️⃣ Criar o arquivo .env e adicionar suas chaves de API


GOOGLE_API_KEY=AIzaSyCRI5wnhj1gqy3O2wg3wE_uEaRNpoSHAko
MISTRAL_API_KEY=N8qK57AYYdyUlfgRjF7Gr1VFOSRhWb7g
DEEPSEEK_API_KEY=sk-a7a3354a521c47a1bc786d6f73673d51



5️⃣ Executar o projeto

python main.py

📊 Como Funciona

🔹 Coleta de Respostas

Cada modelo recebe a mesma pergunta e gera sua resposta:

responses = {
    "Gemini": get_gemini_response(question),
    "Mistral": get_mistral_response(question),
    "Ollama (Mistral)": get_ollama_response(question),
    "DeepSeek": get_deepseek_response(question),
}

🔹 Análise das Respostas

A função analyze_responses() avalia as respostas com base em:

Clareza e coerência (frases bem estruturadas)

Precisão (comparação com um texto de referência)

Criatividade e profundidade (presença de exemplos e argumentos)

Consistência gramatical (uso do LanguageTool)

🔹 Normalização das Notas

Os escores são normalizados para uma escala de 0 a 10.

results = normalize_scores(results)

🔹 Ranking das Respostas

O Gemini classifica as respostas com base nos critérios acima.

ranking_result = rank_responses_with_gemini(responses)

📜 Exemplo de Saída

🔹 Gemini:
A Inteligência Artificial é...

🔹 Mistral:
A IA pode ser definida como...

🔹 Ollama (Mistral):
Inteligência Artificial é...

🔹 DeepSeek:
A IA é uma área da ciência da computação...

🏆 Ranking das respostas:
1. Gemini - Melhor clareza e precisão
2. DeepSeek - Boa profundidade e criatividade
3. Mistral - Resposta coerente, mas genérica
4. Ollama - Resposta mais curta e superficial

 Desenvolvido por Carolyne
