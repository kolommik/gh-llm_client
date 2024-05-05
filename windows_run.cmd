@echo off
call .venv/Scripts/activate
streamlit --version
streamlit run app/streamlit_app.py
