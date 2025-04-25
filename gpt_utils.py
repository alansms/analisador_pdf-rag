# gpt_utils.py
import os
from openai import OpenAIError  # Impo
from langchain_openai import OpenAI
# from langchain_openai.embeddings import OpenAIEmbeddings  # Importação corrigidartação genérica para lidar com erros do OpenAIda para lidar com erros do OpenAI
from dotenv import load_dotenv

def query_gpt(prompt: str, model="gpt-3.5-turbo") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente especialista em IA e RAG."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=512
        )
        return r.choices[0].message.content.strip()
    except OpenAIError as e:  # Captura erros genéricos da biblioteca OpenAI
        return f"Erro ao acessar a API OpenAI: {str(e)}"
