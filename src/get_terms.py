import pandas as pd
import re
from collections import Counter

# Минимальный список стоп-слов
STOPWORDS = {
    "the", "and", "of", "in", "to", "its","a", "for", "with", "on", "by",
    "is", "are", "was", "were", "be", "this", "that", "as", "an",
    "we", "our", "their", "has", "have", "had",
    "patients", "study", "studies", "results", "methods",
    "may", "can", "could", "also", "used", "using"
}

# Регулярка под биомедицинские сущности
BIOMED_PATTERN = re.compile(
    r"\b[a-zA-Z]{2,}[0-9]{0,3}\b|"      # BACE1, CD33
    r"\b[a-zA-Z]+-[a-zA-Z]+\b|"        # beta-amyloid
    r"\b[a-zA-Z]{6,}\b"                # neuroinflammation
)

def extract_biomedical_terms(text):
    # Извлечение токенов из текста
    tokens = BIOMED_PATTERN.findall(text.lower())
    return [
        t for t in tokens
        if t not in STOPWORDS and len(t) >= 4  # Фильтрация стоп-слов и коротких токенов
    ]

def main():
    # Чтение данных из CSV файла
    df = pd.read_csv("data/pros_chunks.csv")

    all_terms = []

    # Обработка каждого текста в DataFrame
    for text in df["text"]:
        all_terms.extend(extract_biomedical_terms(text))

    # Подсчет частоты терминов
    term_freq = Counter(all_terms)

    # Создание DataFrame для частоты терминов
    biomedical_df = (
        pd.DataFrame(term_freq.items(), columns=["term", "frequency"])
        .sort_values("frequency", ascending=False)
        .reset_index(drop=True)
    )

    # --- вывод в консоль ---
    print("\nTop biomedical terms (candidate targets & mechanisms):\n")
    for _, row in biomedical_df.head(30).iterrows():
        print(f"{row.term:25s} {row.frequency}")

    # --- сохраняем для следующего шага ---
    biomedical_df.to_csv(
        "data/bio_terms.csv",
        index=False
    )

    print("\nSaved: data/bio_terms.csv")

if __name__ == "__main__":
    main()
