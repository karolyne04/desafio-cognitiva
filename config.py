from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

# Obter as chaves
google_key = os.getenv("GOOGLE_API_KEY")

mistral_key = os.getenv("MISTRAL_API_KEY") 

deepseek_key = os.getenv("DEEPSEEK_API_KEY")
