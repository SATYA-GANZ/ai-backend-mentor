# main.py (Versi Final dengan Impor yang Benar)

import os
import google.generativeai as genai
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
# --- INI BARIS YANG DIPERBAIKI ---
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# ------------------------------------

load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY tidak ditemukan.")

genai.configure(api_key=api_key)
model_generatif = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI(title="AI Mentor API v4.1 (Corrected)")

print("Memuat database vektor dari folder 'db'...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
db = Chroma(persist_directory="./db", embedding_function=embeddings)
print("Database vektor berhasil dimuat.")

@app.get("/")
def root():
    return {"status": "Server AI Mentor v4.1 (Corrected) berjalan!"}

@app.get("/ask-persona")
def tanya_persona(pertanyaan: str, persona: str):
    if persona.lower() == "digital product":
        print("Menjalankan pencarian di ChromaDB...")
        retriever = db.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(pertanyaan)
        
        konteks = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        system_instruction = "Kamu adalah Mentor Produk Digital yang ahli. kamu flexibel dalam menjawab pertanyaan apapun terkait produk digital, tetapi cari terlebih dahulu jawaban dari konteks yang diberikan lalu kombinasikan saja dengan dataset llm mu. intinya flexibel dan jangan terlalu terikat dan terpaku pada konteks RAG yang diberikan kepadamu"
        
        final_prompt = [system_instruction, "--- KONTEKS RELEVAN ---", konteks, "--- PERTANYAAN PENGGUNA ---", pertanyaan]

        response = model_generatif.generate_content(final_prompt)
        return {"persona_digunakan": "Digital Product (RAG-Chroma)", "jawaban_ai": response.text}
    else:
        # Logika untuk persona lain
        system_instruction = "Kamu adalah mentor AI general... yang bisa menjawab pertanyaan apapun"
        if persona.lower() == "excel":
            system_instruction = "Kamu adalah Excel-Sensei. kamu adalah jenius excel dan juga jenius dalam mentoring atau mengajar excel."
        elif persona.lower() == "marketing":
            system_instruction = "Kamu adalah MarkeTrix..., sangat ahli dan jenius dalam membuat strategi digital marketing, serta pengetahuan luas dan jenius mengenai marketing maupun digital marketing."
        
        response = model_generatif.generate_content([system_instruction, pertanyaan])
        return {"persona_digunakan": persona, "jawaban_ai": response.text}
        