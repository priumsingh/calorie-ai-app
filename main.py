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
    try:
        contents = await file.read()

        # 🔥 Temporary stable detection (no external API)
        # You can upgrade later

        filename = file.filename.lower()

        if "chicken" in filename:
            detected = ["chicken"]
        elif "pizza" in filename:
            detected = ["pizza"]
        elif "tea" in filename:
            detected = ["tea"]
        else:
            detected = ["meal"]

        return {
            "items": [{"name": item, "qty": 1} for item in detected]
        }

    except Exception as e:
        return {
            "items": [{"name": "meal", "qty": 1}],
            "error": str(e)
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
