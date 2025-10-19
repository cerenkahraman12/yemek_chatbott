# qa_local.py
import os
from dotenv import load_dotenv
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ .env dosyasında GEMINI_API_KEY bulunamadı.")

genai.configure(api_key=API_KEY)

EMBED_MODEL_LOCAL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gemini-2.0-flash-exp"

class MealChatbotLocal:
    def __init__(self, db_path="./chroma_db_local"):
        self.model = SentenceTransformer(EMBED_MODEL_LOCAL)
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection("menus_local")

    def ask(self, query: str):
        q_emb = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=3
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context_texts = []
        for doc, meta in zip(documents, metadatas):
            name = meta.get("name", "Bilinmeyen Yemek")
            desc = meta.get("description", "")
            context_texts.append(f"- {name}: {desc}")

        context = "\n".join(context_texts)

        prompt = f"""
Kullanıcı şu soruyu sordu: "{query}"

Aşağıda bazı yemek kayıtları var:
{context}

Bu bilgilere dayanarak kullanıcının isteğine uygun en iyi yemekleri öner.
Yemek isimleri, kısa açıklama ve neden uygun olduklarını belirt.
Cevabını Türkçe, arkadaşça bir tonda yaz.
"""

        response = genai.GenerativeModel(LLM_MODEL).generate_content(prompt)
        return response.text
