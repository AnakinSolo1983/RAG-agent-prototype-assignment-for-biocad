import streamlit as st  # Импортируем библиотеку Streamlit
from rag import RAGAgent  # Импортируем RAGAgent из библиотеки pipe

# Настройка конфигурации страницы Streamlit
st.set_page_config(
    page_title="Alzheimer RAG Assistant",  # Заголовок страницы
    layout="wide"  # Широкий макет страницы
)

# Заголовок приложения
st.title("🧠 Alzheimer Research RAG Assistant")

# Описание приложения
st.markdown(
    "Search potential therapeutic targets for Alzheimer's disease "
    "based on scientific literature."
)

@st.cache_resource  # Кэширование ресурса для оптимизации
def load_agent():
    return RAGAgent()  # Загружаем RAGAgent

agent = load_agent()  # Инициализируем агента

# Поле ввода для исследовательского вопроса
query = st.text_input(
    "Enter your research question:",  # Подсказка для ввода
    placeholder="What are potential targets for Alzheimer's disease treatment?"  # Пример запроса
)

# Кнопка для запуска обработки
if st.button("Run RAG"):
    
    if not query.strip():  # Проверка на пустой ввод
        st.warning("Please enter a query.")  # Предупреждение о пустом запросе
    else:
        with st.spinner("Processing..."):  # Индикатор загрузки
            answer, docs = agent.generate(query)  # Генерация ответа и получение документов

        # Вывод сгенерированного ответа
        st.subheader("📌 Generated Answer")
        st.write(answer)

        # Вывод полученных источников
        st.subheader("Retrieved Sources")
        for i, d in enumerate(docs, 1):  # Перебор документов
            st.markdown(
                f"**{i}. {d['title']}**  \nPMID: {d['pmid']}"  # Форматированный вывод заголовка и PMID
            )
