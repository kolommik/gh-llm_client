@echo off
call .venv/Scripts/activate
streamlit --version
streamlit run app/main.py
