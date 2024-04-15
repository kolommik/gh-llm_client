import os
import datetime
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from openai import OpenAI
from app.utils import load_settings, save_settings

# ===========================================================
# Загрузка ключей
a = load_dotenv(find_dotenv())  # read local .env file
openai_api_key = os.environ['OPENAI_API_KEY']

# ===========================================================
# Загрузка настроек при запуске приложения
settings = load_settings()
folder_path = settings.get("folder_path", "")
target_extensions = settings.get("target_extensions", "")
always_include = settings.get("always_include", "")
excluded_dirs = settings.get("excluded_dirs", "")
system_prompt = settings.get("system_prompt", "")

# ===========================================================
# Настройки
st.sidebar.title("Настройки")

# Поля ввода для настроек
folder_path = st.sidebar.text_input(
    "Folder path", folder_path, help="Введите путь к директории"
)
target_extensions = st.sidebar.text_input(
    "Target extensions",
    target_extensions,
    help="Введите расширения через запятую, например: .py,.txt,.md",
)
always_include = st.sidebar.text_input(
    "Always include files", always_include, help="Введите имена файлов через запятую"
)
excluded_dirs = st.sidebar.text_input(
    "Excluded directories", excluded_dirs, help="Введите директории через запятую"
)
system_prompt = st.sidebar.text_area("System prompt", system_prompt)

# Кнопка для загрузки настроек из файла
load_button = st.sidebar.button("Загрузить настройки")
if load_button:
    settings = load_settings()
    folder_path = settings.get("folder_path", "")
    target_extensions = settings.get("target_extensions", "")
    always_include = settings.get("always_include", "")
    excluded_dirs = settings.get("excluded_dirs", "")
    system_prompt = settings.get("system_prompt", "")

# Кнопка для сохранения настроек в файл
save_button = st.sidebar.button("Сохранить настройки")
if save_button:
    save_settings(
        folder_path, target_extensions, always_include, excluded_dirs, system_prompt
    )
    st.success("Настройки сохранены в файл settings.json")


# st.write(f"Значение x: {x}")

# ===========================================================
# Основной интерфейс
st.title("💬 Вопрос")

# Функция для добавления лога
def add_log(message):
    if "log" not in st.session_state:
        st.session_state["log"] = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["log"].append(f"{timestamp} - {message}")


# tabs = st.tabs(["💬 Чат", "Лог"])


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content


    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    add_log("Ответ ассистента отправлен.")


# Кнопка для показа логов
if st.button('Показать логи'):
    st.text_area("Логи системы:", value="\n".join(st.session_state["log"]), height=300)

