from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "Project": "Aurora",
        "Status": "Online",
        "Version": os.getenv("APP_VERSION", "v1.0.0")
    }

@app.get("/predict")
def predict(value: float):
    prediction = value * 0.85 
    return {"input": value, "prediction": prediction}
