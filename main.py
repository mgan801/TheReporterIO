from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow your dashboard JS to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Serve the dashboard
# -----------------------------
@app.get("/dashboard")
def dashboard():
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except Exception as e:
        return HTMLResponse(f"Error loading dashboard: {e}", status_code=500)

# -----------------------------
# Upload endpoint
# -----------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    # Basic KPIs
    total_sales = df["Sales"].sum()
    avg_sales = df["Sales"].mean()
    row_count = len(df)

    kpis = {
        "total_sales": float(total_sales),
        "avg_sales": float(avg_sales),
        "row_count": int(row_count)
    }

    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "kpis": kpis
    }

# -----------------------------
# Transform endpoint
# -----------------------------
@app.post("/transform")
async def transform_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    # Example transformation: return rows as JSON
    rows = df.to_dict(orient="records")

    return {"rows": rows}

# -----------------------------
# Root redirect
# -----------------------------
@app.get("/")
def root():
    return HTMLResponse(
        "<h2>theReporter.io API is running</h2><p>Visit /dashboard</p>"
    )
