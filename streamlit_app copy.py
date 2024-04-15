import streamlit as st

# st.title("Привет, Streamlit!")

# if st.button("Нажми меня"):
#     st.write("Добро пожаловать в мир Streamlit!")

# Текст с раскрашенными символами
colored_text = "Это <span style='color:red'>пример</span> <span style='color:green'>текста</span> с раскрашенными символами."


# Функция для отображения всплывающей подсказки
def show_tooltip(text, tooltip_text):
    st.write(
        f'<div style="position:relative">{text}<span style="position:absolute; background-color:gray; color:white; padding:5px; border-radius:5px">{tooltip_text}</span></div>',
        unsafe_allow_html=True,
    )


# Создаем переключатель
show_colored_text = st.checkbox("Показать раскрашенный текст")

# Отображение текста
if show_colored_text:
    st.markdown(colored_text, unsafe_allow_html=True)
else:
    st.write("Это пример текста без раскраски.")

# Отображение текстового поля с всплывающими подсказками
text_input = st.text_area("Введите текст")
for i, char in enumerate(text_input):
    show_tooltip(char, f"Символ {i+1}: {char}")
