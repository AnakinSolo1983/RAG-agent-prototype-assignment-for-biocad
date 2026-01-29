import pandas as pd  # Импортируем библиотеку pandas для работы с данными
import re  # Импортируем библиотеку re для работы с регулярными выражениями

def clean_text(text):
    if not isinstance(text, str):  # Проверяем, является ли текст строкой
        return ""

    text = text.lower()  # Приводим текст к нижнему регистру
    text = re.sub(r"\s+", " ", text)  # Заменяем несколько пробелов на один
    text = re.sub(r"[^a-z0-9.,()%-]", " ", text)  # Удаляем нежелательные символы
    return text.strip()  # Удаляем пробелы в начале и конце

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()  # Разбиваем текст на слова
    if len(words) < 20:  # Проверяем, достаточно ли слов для разбиения
        return []

    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]  # Создаем часть заданного размера
        chunks.append(" ".join(chunk))  # Объединяем слова в часть
        i += chunk_size - overlap  # Перемещаем индекс для следующей части

    return chunks

def main():
    df = pd.read_csv("data/pubmed_articles.csv")  # Читаем CSV-файл

    records = []

    for _, row in df.iterrows():  # Итерируем по каждой строке в DataFrame
        clean_abs = clean_text(row["abstract"])  # Очищаем текст аннотации

        if not clean_abs:  # Пропускаем, если очищенная аннотация пуста
            continue

        chunks = chunk_text(clean_abs)  # Разбиваем очищенную аннотацию на части

        for chunk in chunks:
            records.append({
                "pmid": row["pmid"],  # Сохраняем PMID
                "title": row["title"],  # Сохраняем заголовок
                "text": chunk  # Сохраняем часть текста
            })

    out_df = pd.DataFrame(records)  # Создаем DataFrame из записей

    if out_df.empty:  # Проверяем, были ли созданы части
        raise ValueError("Не было создано текстовых частей. Проверьте входные данные.")

    out_df.to_csv("data/pros_chunks.csv", index=False)  # Сохраняем части в новый CSV-файл
    print(f"Сохранено {len(out_df)} текстовых частей")  # Выводим количество сохраненных частей

if __name__ == "__main__":
    main()  # Выполняем основную функцию
