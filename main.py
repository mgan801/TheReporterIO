from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

# Allow dashboard to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def compute_basic_kpis(df):
    kpis = {}
    if "Sales" in df.columns:
        kpis["total_sales"] = float(df["Sales"].sum())
        kpis["avg_sales"] = float(df["Sales"].mean())
    kpis["row_count"] = len(df)
    return kpis

@app.get("/dashboard")
def get_dashboard():
    with open("dashboard.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(BytesIO(content))
    kpis = compute_basic_kpis(df)

    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "kpis": kpis
    }

@app.post("/transform")
async def transform_file(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(BytesIO(content))

    df["Sales_x2"] = df["Sales"] * 2

    return {
        "columns": df.columns.tolist(),
        "rows": df.to_dict(orient="records")
    }
