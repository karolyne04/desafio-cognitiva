import google.generativeai as genai
from config import google_key

# 🔹 Configuração da API do Gemini
genai.configure(api_key=google_key)


def rank_responses_with_gemini(responses):
    """
    Envia as respostas dos modelos para o Gemini e solicita um ranking baseado em clareza, coerência, precisão e criatividade.
    """
    prompt = """
    Aqui estão várias respostas para a mesma pergunta, geradas por diferentes modelos de linguagem.
    Sua tarefa é analisá-las e ranqueá-las com base nos seguintes critérios:

    - Clareza (a resposta é fácil de entender?)
    - Coerência (as ideias fazem sentido juntas?)
    - Precisão da informação (a resposta é correta?)
    - Criatividade ou profundidade da resposta

    Respostas recebidas:
    """

    for model, response in responses.items():
        prompt += f"\n🔹 {model}: {response}\n"

    prompt += "\nAgora, analise e forneça um ranking no seguinte formato:\n\n"
    prompt += "1. [Modelo] - Justificativa\n2. [Modelo] - Justificativa\n3. [Modelo] - Justificativa\n"

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text if response else "Erro ao obter ranking do Gemini."
    except Exception as e:
        return f"Erro ao obter ranking do Gemini: {e}"
