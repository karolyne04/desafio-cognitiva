import google.generativeai as genai
from mistralai.client import MistralClient
import requests
from config import google_key, mistral_key, deepseek_key
import re
import language_tool_python
import numpy as np


# 🔹 Configuração da API do Gemini
genai.configure(api_key=google_key)

# 🔍 Função para obter resposta do Gemini
def get_gemini_response(question: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        return response.text if response else "Erro ao obter resposta do Gemini."
    except Exception as e:
        return f"Erro Gemini: {str(e)}"

# 🔍 Função para obter resposta do Mistral
def get_mistral_response(question: str) -> str:
    try:
        client = MistralClient(api_key=mistral_key)
        response = client.chat(
            model="mistral-medium",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro Mistral: {str(e)}"

# 🔍 Função para obter resposta do Ollama
def get_ollama_response(question: str) -> str:
    try:
        url = "http://127.0.0.1:11434/api/generate"
        data = {"model": "mistral", "prompt": question, "stream": False}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get("response", "Erro: Resposta vazia.")
        return f"Erro: {response.text}"
    except requests.exceptions.ConnectionError:
        return "Erro Ollama: Servidor não está rodando. Execute 'ollama run mistral'."
    except Exception as e:
        return f"Erro Ollama: {str(e)}"

# 🔍 Função para obter resposta do DeepSeek
def get_deepseek_response(question: str) -> str:
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"}
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": question}], "temperature": 0.7}

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            return "Erro DeepSeek: Chave de API inválida ou sem permissão."
        elif response.status_code == 402:
            return "Erro DeepSeek: Saldo insuficiente. Verifique sua conta."
        return f"Erro DeepSeek: {response.text}"
    except Exception as e:
        return f"Erro DeepSeek: {str(e)}"

# 🔍 Texto de referência para comparação
REFERENCE_TEXT = """
Inteligência Artificial (IA) é um campo da ciência da computação que visa criar sistemas capazes de simular processos de pensamento humano, como aprendizado, raciocínio e resolução de problemas. 
Algumas abordagens incluem redes neurais, aprendizado profundo e algoritmos genéticos. A IA é aplicada em diversas áreas, como saúde, finanças e tecnologia.
"""

# 📊 Função para calcular similaridade entre resposta e texto de referência
def calculate_similarity(response: str, reference: str) -> float:
    response_words = set(response.lower().split())
    reference_words = set(reference.lower().split())
    intersection = len(response_words & reference_words)
    union = len(reference_words)
    return intersection / union if union > 0 else 0

# 📊 Função para analisar respostas dos modelos
def analyze_responses(responses):
    """
    Analisa as respostas dos modelos de IA com base em vários critérios:
    - Clareza e coerência (presença de sentenças bem estruturadas)
    - Precisão da informação (comparação com o texto de referência)
    - Criatividade e profundidade (quantidade de argumentos e exemplos)
    - Consistência gramatical (erros identificados pelo LanguageTool)
    """

    tool = language_tool_python.LanguageTool('pt-BR')

    results = {}

    for model, response in responses.items():
        # 1️⃣ Clareza e coerência: Contar frases bem estruturadas (mínimo 5 palavras)
        sentences = re.split(r'[.!?]', response)
        well_structured_sentences = sum(1 for s in sentences if len(s.split()) >= 5)

        # 2️⃣ Precisão da informação: Comparação com o texto de referência
        precision_score = calculate_similarity(response, REFERENCE_TEXT)

        # 3️⃣ Criatividade e profundidade: Contar número de argumentos/exemplos
        num_arguments = response.lower().count("por exemplo") + response.lower().count("como") + response.lower().count(
            "isto significa")

        # 4️⃣ Consistência gramatical: Verificar erros gramaticais
        grammar_errors = len(tool.check(response))

        # Armazena os resultados antes da normalização
        results[model] = {
            "clareza_coerencia": well_structured_sentences,
            "precisao": precision_score,
            "criatividade_profundidade": num_arguments,
            "gramatica": -grammar_errors  # Quanto menos erros, melhor o score
        }

    # 🔢 Normaliza os scores para uma escala de 0 a 10
    results = normalize_scores(results)

    return results

# 🔢 Função para normalizar os scores entre 0 e 10
def normalize_scores(results):
    criteria = ["clareza_coerencia", "precisao", "criatividade_profundidade", "gramatica"]

    for criterion in criteria:
        scores = [model_scores[criterion] for model_scores in results.values()]
        min_score, max_score = min(scores), max(scores)

        # Evita divisão por zero se todos os valores forem iguais
        if min_score == max_score:
            normalized_scores = [5] * len(scores)  # Se todos forem iguais, atribui um valor médio
        else:
            normalized_scores = [((score - min_score) / (max_score - min_score)) * 10 for score in scores]

        # Atribui os valores normalizados de volta ao dicionário
        for i, model in enumerate(results.keys()):
            results[model][criterion] = round(normalized_scores[i], 2)

    return results
