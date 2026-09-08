from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔢 Calorie Database
CAL_DB = {
    "biryani": 350,
    "pizza": 300,
    "coke": 105,
    "tea": 50,
    "chicken": 250,
    "rice": 200,
    "meal": 400
}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    filename = file.filename.lower()

    # 🔥 Simple smart detection based on filename (for now)
    if "chicken" in filename:
        detected = ["chicken", "meal"]
    elif "pizza" in filename:
        detected = ["pizza"]
    elif "tea" in filename:
        detected = ["tea"]
    else:
        detected = ["meal"]

    return {
        "items": [
            {"name": item, "qty": 1} for item in detected
        ]
    }
# 🔢 CALCULATE CALORIES
@app.post("/calculate")
def calculate(data: dict):
    total = 0
    result = []

    for item in data.get("items", []):
        name = item.get("name", "meal")
        qty = item.get("qty", 1)

        cal = CAL_DB.get(name, 100) * qty
        total += cal

        result.append({
            "name": name,
            "calories": cal
        })

    return {
        "items": result,
        "total": total
    }
