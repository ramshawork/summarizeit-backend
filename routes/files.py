from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from utils.file_helper import read_file_content
from utils.ai_helper import generate_summary_from_text, chat_with_document
import os

router = APIRouter()

# 📌 Summarize file (existing)
@router.post("/summarize-file")
async def summarize_file(
    file: UploadFile = File(...), 
    word_limit: int = Form(100), 
    mode: str = Form("summary"), 
    language: str = Form("English")
):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")

    content = await read_file_content(file)
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not set")

    result = generate_summary_from_text(content, word_limit, api_key, mode, language)
    return {"result": result}


# 📌 Chat with Document (new)
@router.post("/chat-with-file")
async def chat_with_file(
    file: UploadFile = File(...),
    query: str = Form(...),
    language: str = Form("English")
):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")

    content = await read_file_content(file)
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not set")

    result = chat_with_document(query, content, api_key, language)
    return {"result": result}
