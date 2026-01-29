import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Читаем данные из CSV файла
df = pd.read_csv("data/chunks_enriched.csv")

# Загружаем предобученную модель для преобразования предложений
model = SentenceTransformer("all-MiniLM-L6-v2")

# Генерируем векторы для каждого предложения в данных
embeddings = model.encode(
    df["text"].tolist(),
    show_progress_bar=True  # Показываем прогресс выполнения
)

# Получаем размерность векторов
dim = embeddings.shape[1]
# Создаем индекс FAISS для хранения векторов
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))  # Добавляем векторы в индекс

# Сохраняем индекс в файл
faiss.write_index(index, "data/faiss.index")

# Сохраняем метаданные в файл
with open("data/metadata.pkl", "wb") as f:
    pickle.dump(df.to_dict("records"), f)

print("Vector store saved")  # Выводим сообщение о завершении
