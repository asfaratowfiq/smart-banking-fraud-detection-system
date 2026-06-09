echo off

echo Starting Redis...
docker start redis-local

timeout /t 2 > nul

echo Starting Celery Worker...
start cmd /k "call .venv\Scripts\activate && python -m celery -A app.workers.celery_app.celery_app worker --pool=solo --loglevel=info"

timeout /t 2 > nul

echo Starting FastAPI...
start cmd /k "call .venv\Scripts\activate && uvicorn main:app --reload"

timeout /t 2 > nul

echo Starting Streamlit...
start cmd /k "call .venv\Scripts\activate && streamlit run ui/dashboard.py"

echo.
echo ====================================
echo All Services Started
echo ====================================

pause
