from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from utils.ai_helper import generate_summary_from_text

# ✅ Router define karna zaruri hai
router = APIRouter()

# Request body model
class SummarizeRequest(BaseModel):
    text: str
    word_limit: int = 100
    mode: str = "summary"   # summary | keypoints | simplify | title | faqs | chat
    language: str = "English"   # (default English)

# ✅ API endpoint
@router.post("/summarize-text")
async def summarize_text(payload: SummarizeRequest):
    text = payload.text
    if not text or text.strip() == "":
        raise HTTPException(status_code=400, detail="Text is required")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not set")

    try:
        result = generate_summary_from_text(
            text,
            payload.word_limit,
            api_key,
            payload.mode,
            payload.language
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
