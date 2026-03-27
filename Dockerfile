FROM python:3.9-slim
WORKDIR /app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
