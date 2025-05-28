@echo off
cd /d "C:\Users\Kikolândia\Desktop\Projeto_skava\dashboard_kiko"
call venv\Scripts\activate
venv\Scripts\streamlit.exe run app.py
pause
