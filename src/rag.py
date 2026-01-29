import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Инициализация класса RAGAgent
class RAGAgent:
    def __init__(self):
        # ---------- Извлекатель ----------
        self.embedder = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.index = faiss.read_index("data/faiss.index")

        with open("data/metadata.pkl", "rb") as f:
            self.docs = pickle.load(f)

        # ---------- Генератор ----------
        self.model_name = "google/flan-t5-base"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.generator = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name
        )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.generator.to(self.device)

    # -------------------------------
    def retrieve(self, query, k=3):
        # Код для извлечения документов
        q_emb = self.embedder.encode(
            [query],
            normalize_embeddings=True
        )

        distances, indices = self.index.search(
            np.array(q_emb, dtype=np.float32), k
        )

        results = []
        for idx in indices[0]:
            if idx < len(self.docs):
                results.append(self.docs[idx])

        return results

    # -------------------------------
    def generate(self, query):
        # Код для генерации ответа
        docs = self.retrieve(query)

        context = "\n".join(
            [f"- {d['text']}" for d in docs]
        )

        prompt = f"""
Вы - помощник в области биомедицинских исследований.

Основываясь только на приведенном ниже контексте, ответьте на вопрос.
Цитируйте источники, используя PMID.

Контекст:
{context}

Вопрос:
{query}

Ответ:
""".strip()

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        outputs = self.generator.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False
        )

        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return answer, docs
