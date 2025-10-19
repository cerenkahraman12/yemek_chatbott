# 🍽️ Yemek Öneri Chatbotu (RAG Temelli)

## 📘 Proje Amacı
Bu proje, **Retrieval-Augmented Generation (RAG)** mimarisi kullanarak çalışan bir yemek öneri chatbot’u geliştirmeyi amaçlamaktadır.  
Kullanıcı, doğal dilde yemek veya diyet tercihini yazdığında, sistem veritabanındaki yemek kayıtlarını **yerel embedding modeli**yle arar ve en uygun sonuçları **Gemini 2.0 Flash** modeliyle anlamlı ve akıcı bir Türkçe cevap hâline getirir.  

---

## 🥗 Veri Seti
Veri seti `menus.csv` dosyasından alınmıştır.  
Her satır bir yemeği temsil eder ve aşağıdaki bilgileri içerir:

| Sütun | Açıklama |
|--------|-----------|
| `id` | Yemeğin benzersiz kimliği |
| `name` | Yemeğin adı |
| `category` | Yemek türü (çorba, ana yemek, tatlı vb.) |
| `ingredients` | İçerik listesi |
| `description` | Yemeğin kısa açıklaması |
| `tags` | Etiketler (vegan, düşük kalorili, etli, vs.) |

Bu veri seti, örnek menü kayıtlarından oluşturulmuş ve chatbot’un test edilmesi için el ile düzenlenmiştir.  

---

## ⚙️ Kullanılan Teknolojiler

| Katman | Teknoloji | Açıklama |
|--------|------------|----------|
| **Embedding (Bilgi Arama)** | `sentence-transformers/all-MiniLM-L6-v2` | Kullanıcının sorgusu ve yemek açıklamaları vektörlere dönüştürülür. |
| **Veritabanı** | ChromaDB | Embedding’ler üzerinde benzerlik araması yapılır. |
| **Cevap Üretimi** | Gemini 2.0 Flash (Google Generative AI) | En uygun yemekleri Türkçe, anlamlı ve açıklayıcı biçimde önerir. |
| **Arayüz** | Streamlit | Kullanıcıların sohbet arayüzü üzerinden etkileşime girmesini sağlar. |
| **Dil** | Python | Tüm sistem Python ile yazılmıştır. |

---

## 🧠 Mimari Akış (RAG Pipeline)

1. **Kullanıcı Sorgusu:**  
   Kullanıcı “Vegan akşam yemeği önerir misin?” gibi bir soru sorar.

2. **Yerel Embedding:**  
   `sentence-transformers` modeli sorguyu embedding’e dönüştürür.

3. **Retriever (ChromaDB):**  
   En benzer yemek kayıtları bulunur.

4. **Generator (Gemini 2.0 Flash):**  
   Bulunan yemek bilgileri Gemini modeline verilerek Türkçe yanıt üretilir.

5. **Arayüz:**  
   Sonuçlar Streamlit üzerinden kullanıcıya gösterilir.

---

## 🧩 Proje Dosya Yapısı
yemek_chatbot/
│
├── app.py # Streamlit arayüz dosyası
├── ingest_local.py # Yerel embedding ile veritabanı oluşturma
├── qa_local.py # Sorgu + Gemini yanıt üretimi
├── menus.csv # Yemek veri seti
├── chroma_db_local/ # Yerel vektör veritabanı
├── requirements.txt # Gerekli Python kütüphaneleri
└── .env # Gemini API anahtarı
# Yemek_ChatBot
