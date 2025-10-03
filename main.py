from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import ai, files   # ✅ ab backend. lagane ki zarurat nahi
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Summarize AI - FastAPI Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(files.router, prefix="/api/files", tags=["files"])


@app.get("/")
def root():
    return {"message": "FastAPI backend running"}
