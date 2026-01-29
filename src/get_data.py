from Bio import Entrez
import pandas as pd
from tqdm import tqdm

# Укажите свой адрес электронной почты
Entrez.email = "your_email@example.com"

# Запросы для поиска
QUERIES = [
    "Alzheimer's disease targets",
    "Alzheimer therapeutic targets",
    "Alzheimer drug targets"
]

# Максимальное количество результатов для каждого запроса
MAX_RESULTS_PER_QUERY = 30

# Функция для поиска в PubMed
def search_pubmed(query, max_results):
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results
    )
    record = Entrez.read(handle)
    return record["IdList"]

# Функция для получения статьи по PMID
def fetch_article(pmid):
    handle = Entrez.efetch(
        db="pubmed",
        id=pmid,
        rettype="abstract",
        retmode="xml"
    )
    record = Entrez.read(handle)

    article = record["PubmedArticle"][0]["MedlineCitation"]["Article"]

    title = article.get("ArticleTitle", "")
    abstract = " ".join(
        article.get("Abstract", {}).get("AbstractText", [])
    )

    return {
        "pmid": pmid,
        "title": title,
        "abstract": abstract
    }

# Основная функция
def main():
    all_pmids = set()

    # Поиск статей по всем запросам
    for q in QUERIES:
        pmids = search_pubmed(q, MAX_RESULTS_PER_QUERY)
        all_pmids.update(pmids)

    articles = []
    # Получение информации о каждой статье
    for pmid in tqdm(all_pmids):
        try:
            articles.append(fetch_article(pmid))
        except Exception:
            continue

    # Сохранение данных в CSV файл
    df = pd.DataFrame(articles)
    df.to_csv("data/bio_articles.csv", index=False)

# Запуск основной функции
if __name__ == "__main__":
    main()
