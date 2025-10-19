# qa.py (Chroma yeni sürüm + Gemini LLM)
import os
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ .env dosyasında GEMINI_API_KEY bulunamadı.")

genai.configure(api_key=API_KEY)

EMBED_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-2.0-flash-exp"

def get_embedding(text: str):
    resp = genai.embed_content(model=EMBED_MODEL, content=text)
    return resp["embedding"]

class MealChatbot:
    def __init__(self, db_path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection("menus")

    def ask(self, query: str):
        # Sorgunun embedding'ini al
        q_emb = get_embedding(query)

        # Chroma'dan en benzer 3 sonucu getir
        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=3
        )

        # Sonuçları bir metin haline getir
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context_texts = []
        for doc, meta in zip(documents, metadatas):
            name = meta.get("name", "Bilinmeyen Yemek")
            desc = meta.get("description", "")
            context_texts.append(f"- {name}: {desc}")

        context = "\n".join(context_texts)

        # Gemini için prompt
        prompt = f"""
Kullanıcı şu soruyu sordu: "{query}"

Aşağıda bazı yemek kayıtları var:
{context}

Bu bilgilere dayanarak kullanıcının isteğine uygun en iyi yemekleri öner.
Yemek isimleri, kısa açıklama ve neden uygun olduklarını belirt.
Cevabını Türkçe, doğal ve arkadaşça bir tonda yaz.
"""

        response = genai.GenerativeModel(LLM_MODEL).generate_content(prompt)
        return response.text
