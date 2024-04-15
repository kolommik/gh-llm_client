import streamlit as st
import streamlit.components.v1 as components

# st.title("Привет, Streamlit!")

# # Настройки
# st.sidebar.title("Настройки")
# folder_path = st.sidebar.text_input("Folder path")
# target_extensions = st.sidebar.text_input(
#     "Target extensions", help="Введите расширения через запятую, например: .py,.txt,.md"
# )
# always_include = st.sidebar.text_input(
#     "Always include files", help="Введите имена файлов через запятую"
# )
# excluded_dirs = st.sidebar.text_input(
#     "Excluded directories", help="Введите директории через запятую"
# )
# system_prompt = st.sidebar.text_area("System prompt")

# # Основной интерфейс
# st.title("Чат-диалог")
# question = st.text_area("Введите ваш вопрос")
# if st.button("Отправить"):
#     # Здесь можно добавить ваш код для обработки вопроса и получения ответа
#     answer = "Это пример ответа на ваш вопрос."
#     st.text_area("Ответ", value=answer, height=200)

# ====================================================
# ====================================================
# ====================================================
# ====================================================

# # Создаем вкладки
# tabs = st.tabs(["Настройки", "Чат"])

# # Вкладка "Настройки"
# with tabs[0]:
#     st.header("Настройки")
#     folder_path = st.text_input("Folder path")
#     target_extensions = st.text_input(
#         "Target extensions",
#         help="Введите расширения через запятую, например: .py,.txt,.md",
#     )
#     always_include = st.text_input(
#         "Always include files", help="Введите имена файлов через запятую"
#     )
#     excluded_dirs = st.text_input(
#         "Excluded directories", help="Введите директории через запятую"
#     )
#     system_prompt = st.text_area("System prompt")

#     show_content = st.checkbox("Показать содержимое")
#     if show_content:
#         st.write("Это содержимое, которое показывается при нажатии на checkbox")

# # Вкладка "Чат"
# with tabs[1]:


#     # with st.expander("Раскрывающийся заголовок"):
#     #     # Содержимое, которое будет скрыто/показано при раскрытии
#     #     st.write("Это раскрывающееся содержимое")

#     st.header("Чат-диалог")
#     question = st.text_area("Введите ваш вопрос")
#     if st.button("Отправить"):
#         # Здесь можно добавить ваш код для обработки вопроса и получения ответа
#         answer = "Это пример ответа на ваш вопрос."
#         st.text_area("Ответ", value=answer, height=200)

#         # colored_answer = "Это пример <span style='color:red'>ответа</span> на ваш <span style='color:green'>вопрос</span>."
#         # st.markdown(colored_answer, unsafe_allow_html=True)
# ====================================================
# ====================================================
# ====================================================
# ====================================================

# # HTML-код для раскрывающегося списка
# html = """
# <div>
#   <details>
#     <summary>Раскрывающийся заголовок</summary>
#     <p>Это раскрывающееся содержимое</p>
#   </details>
# </div>
# """

# # CSS-стили для форматирования раскрывающегося списка
# css = """
# <style>
# details {
#   background-color: #f0f0f0;
#   padding: 10px;
#   border-radius: 5px;
#   cursor: pointer;
# }

# details > summary {
#   font-weight: bold;
# }
# </style>
# """

# # Объединение HTML и CSS
# html_with_css = css + html

# # Отображение раскрывающегося списка в Streamlit
# components.html(html_with_css, height=200)

# ====================================================
# ====================================================
# ====================================================
# ====================================================

# # Текст для отображения
# text_to_display = "Этот текст можно скопировать в буфер обмена."

# # HTML-код с JavaScript для копирования текста
# html = f"""
# <div>
#   <span id="text-to-copy">{text_to_display}</span>
#   <button onclick="copyText()">Скопировать в буфер</button>
# </div>

# <script>
# function copyText() {{
#   const textToCopy = document.getElementById("text-to-copy").innerText;
#   navigator.clipboard.writeText(textToCopy)
#     .then(() => alert("Текст скопирован в буфер обмена!"))
#     .catch((error) => alert("Ошибка при копировании текста: " + error));
# }}
# </script>
# """

# # Отображение HTML-компонента в Streamlit
# components.html(html, height=100)

# # Этот текст можно скопировать в буфер обмена.

# ====================================================
# ====================================================
# ====================================================
# ====================================================
# ====================================================


# Текст для отображения с раскраской
colored_text = "Это <span class='word'>пример</span> <span class='word'>текста</span> с <span class='word'>подсказками</span> на <span class='word'>словах</span>."

# HTML-код с CSS и JavaScript
html = f"""
<div id="text-container">{colored_text}</div>

<style>
.word {{
  position: relative;
  display: inline-block;
}}

.word .tooltip {{
  visibility: hidden;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 150%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
}}

.word:hover .tooltip {{
  visibility: visible;
  opacity: 1;
}}
</style>

<script>
const words = document.querySelectorAll('.word');
words.forEach(word => {{
  const tooltip = document.createElement('span');
  tooltip.classList.add('tooltip');
  tooltip.innerText = word.innerText;
  word.appendChild(tooltip);
}});
</script>
"""

# Отображение HTML-компонента в Streamlit
components.html(html, height=200)


