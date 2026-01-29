import pandas as pd

def main():
    # Считываем CSV-файлы, содержащие текстовые фрагменты и биомедицинские термины
    chunks = pd.read_csv("data/pros_chunks.csv")
    terms = pd.read_csv("data/bio_terms.csv")

    # Фильтруем, чтобы оставить только значимые термины с частотой 20 и более
    important_terms = set(
        terms[terms["frequency"] >= 20]["term"]
    )

    enriched_records = []

    # Итерируем по каждой строке в DataFrame chunks
    for _, row in chunks.iterrows():
        text = row["text"].lower()  # Приводим текст к нижнему регистру
        matched_terms = [
            t for t in important_terms if t in text  # Находим совпадающие термины
        ]

        # Добавляем обогащенную запись в список
        enriched_records.append({
            "pmid": row["pmid"],
            "title": row["title"],
            "text": row["text"],
            "biomedical_terms": ", ".join(matched_terms)  # Объединяем совпадающие термины
        })

    # Создаем DataFrame из обогащенных записей
    enriched_df = pd.DataFrame(enriched_records)

    # Сохраняем обогащенный DataFrame в новый CSV-файл
    enriched_df.to_csv(
        "data/chunks_enriched.csv",
        index=False
    )

    print(
        f"Сохранено {len(enriched_df)} обогащенных фрагментов "
        "в data/chunks_enriched.csv"
    )

if __name__ == "__main__":
    main()
