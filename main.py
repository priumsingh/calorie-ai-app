from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CAL_DB = {
    "biryani": 350,
    "pizza": 300,
    "coke": 105,
    "tea": 50,
    "chicken": 250,
    "rice": 200,
    "meal": 400
}

@app.get("/")
def home():
    return {"message": "Cloud backend running"}

# 🔥 REAL AI (using public hosted model API)
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()

    response = requests.post(
        "https://api-inference.huggingface.co/models/nateraw/food",
        headers={"Authorization": "Bearer YOUR_HF_TOKEN"},
        data=contents
    )

    try:
        result = response.json()
        detected = [x["label"] for x in result[:3]]
    except:
        detected = ["meal"]

    return {
        "items": [{"name": i.lower(), "qty": 1} for i in detected]
    }

@app.post("/calculate")
def calculate(data: dict):
    total = 0
    result = []

    for item in data["items"]:
        cal = CAL_DB.get(item["name"], 100) * item["qty"]
        total += cal
        result.append({
            "name": item["name"],
            "calories": cal
        })

    return {"items": result, "total": total}
