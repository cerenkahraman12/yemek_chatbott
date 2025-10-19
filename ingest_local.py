# ingest_local.py
import os
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import chromadb

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_data(path="menus.csv"):
    df = pd.read_csv(path)
    docs = []
    for _, row in df.iterrows():
        content = f"{row['name']} — {row['category']} — {row['ingredients']} — {row['description']} (tags: {row['tags']})"
        meta = row.to_dict()
        docs.append((str(row['id']), content, meta))
    return docs

def main():
    print(f"Yemekler yükleniyor...")
    docs = load_data("menus.csv")
    texts = [d[1] for d in docs]
    ids = [d[0] for d in docs]
    metadatas = [d[2] for d in docs]

    print("Yerel embedding modeli yükleniyor...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = [model.encode(t) for t in tqdm(texts)]

    client = chromadb.PersistentClient(path="./chroma_db_local")

    try:
        collection = client.get_collection("menus_local")
    except Exception:
        collection = client.create_collection("menus_local")

    try:
        existing = collection.get()
        if existing and len(existing.get("ids", [])) > 0:
            collection.delete(ids=existing["ids"])
    except Exception:
        pass

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print("✅ Yerel embedding ile veritabanı oluşturuldu! ./chroma_db_local")

if __name__ == "__main__":
    main()
