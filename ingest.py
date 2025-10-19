# ingest.py (Chroma yeni API uyumlu)
import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ .env dosyasında GEMINI_API_KEY bulunamadı. Lütfen ekle.")

genai.configure(api_key=API_KEY)

EMBED_MODEL = "models/embedding-001"  # Gemini embedding modeli

def load_data(path="menus.csv"):
    df = pd.read_csv(path)
    docs = []
    for _, row in df.iterrows():
        content = f"{row['name']} — {row['category']} — {row['ingredients']} — {row['description']} (tags: {row['tags']})"
        meta = row.to_dict()
        docs.append((str(row['id']), content, meta))
    return docs

def get_embedding(text: str):
    resp = genai.embed_content(model=EMBED_MODEL, content=text)
    emb = resp.get("embedding")
    if emb is None:
        raise RuntimeError(f"Embedding alınamadı. API yanıtı: {resp}")
    return emb

def main():
    docs = load_data("menus.csv")
    print(f"{len(docs)} yemek yüklendi. Embedding oluşturuluyor...")

    texts = [d[1] for d in docs]
    ids = [d[0] for d in docs]
    metadatas = [d[2] for d in docs]

    # ✅ Yeni Chroma client (v0.5 ve sonrası)
    client = chromadb.PersistentClient(path="./chroma_db")

    # Eğer koleksiyon yoksa oluştur, varsa getir
    try:
        collection = client.get_collection("menus")
    except Exception:
        collection = client.create_collection("menus")

    embeddings = []
    for t in tqdm(texts):
        embeddings.append(get_embedding(t))

    # Önceden aynı id varsa üzerine yazmak için ekleme öncesi temizle
    try:
        existing_ids = [x["id"] for x in collection.get()["metadatas"]]
        for eid in existing_ids:
            collection.delete(ids=[eid])
    except Exception:
        pass

    # Verileri koleksiyona ekle
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print("✅ Ingest tamamlandı! Veritabanı: ./chroma_db")

if __name__ == "__main__":
    main()
