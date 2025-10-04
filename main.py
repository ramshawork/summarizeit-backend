from fastapi import FastAPI, UploadFile, File   
from fastapi.middleware.cors import CORSMiddleware
from routes import ai, files 
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Summarize AI - FastAPI Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can replace * with your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(files.router, prefix="/api/files", tags=["files"])


@app.get("/")
def root():
    return {"message": "FastAPI backend running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        return {"content": contents.decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}

