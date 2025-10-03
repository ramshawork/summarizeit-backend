import google.generativeai as genai
import re

def get_client(api_key: str):
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set")
    genai.configure(api_key=api_key)
    return genai

def build_prompt(text: str, word_limit: int = 100, mode: str = "summary", language: str = "English") -> str:
    """
    Different prompts based on mode
    """
    if mode == "summary":
        return f"Summarize this text in about {word_limit} words in {language}:\n\n{text}"
    elif mode == "keypoints":
        return f"Extract the key points from this text in bullet points in {language}:\n\n{text}"
    elif mode == "simplify":
        return f"Explain the following text in simple easy-to-understand {language}, around {word_limit} words:\n\n{text}"
    elif mode == "title":
        return f"Write a short engaging title in {language} for the following text:\n\n{text}"
    elif mode == "faqs":
        return f"Generate 5 FAQ-style questions and answers in {language} from the following text:\n\n{text}"
    elif mode == "chat":
        return f"You are a helpful assistant. Answer the following user query based on this document in {language}:\n\n{text}"
    else:
        return f"Summarize this text in about {word_limit} words in {language}:\n\n{text}"

def clean_response(text: str) -> str:
    # Markdown symbols hatado
    text = re.sub(r"[*#`>-]", "", text)  
    text = text.replace("\n\n", "\n")  # double newlines fix
    return text.strip()

def generate_summary_from_text(text: str, word_limit: int, api_key: str, mode: str, language: str = "English") -> str:
    """
    Generate AI output based on selected mode & language
    """
    client = get_client(api_key)
    prompt = build_prompt(text, word_limit, mode, language)

    # ✅ Gemini API call (stable way)
    model = client.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

   # Gemini response ka structure safe tarike se handle karo
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return str(response)
    except Exception as e:
        return f"Error parsing AI response: {e}"


def chat_with_document(query: str, document_text: str, api_key: str, language: str = "English") -> str:
    client = get_client(api_key)

    prompt = f"""
    You are an AI assistant. Use the following document to answer the user query.

    Document:
    {document_text[:5000]}   # safety limit

    Question:
    {query}

    Answer in {language}.
    """

    model = client.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else str(response)

