from rank_responses import rank_responses_with_gemini
from llm_comparator import (  # Substitua pelo nome real do seu arquivo
    get_gemini_response,
    get_mistral_response,
    get_ollama_response,
    get_deepseek_response
)

# 📝 Pergunta para os modelos
question = "O que é Inteligência Artificial?"

# 🚀 Obtendo respostas dos modelos
responses = {
    "Gemini": get_gemini_response(question),
    "Mistral": get_mistral_response(question),
    "Ollama (Mistral)": get_ollama_response(question),
    "DeepSeek": get_deepseek_response(question),
}

# 📊 Exibindo respostas
for model, response in responses.items():
    print(f"\n🔹 {model}:\n{response}")

# 🏆 Gerando ranking com o Gemini
ranking_result = rank_responses_with_gemini(responses)
print("\n🏆 Ranking das respostas:\n")
print(ranking_result)
