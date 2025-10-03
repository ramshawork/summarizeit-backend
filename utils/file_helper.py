import PyPDF2
import docx
from fastapi import UploadFile
import io

async def read_file_content(uploaded_file: UploadFile) -> str:
    filename = uploaded_file.filename.lower()
    contents = await uploaded_file.read()
    if filename.endswith('.pdf'):
        # read PDF from bytes
        reader = PyPDF2.PdfReader(io.BytesIO(contents))
        text = []
        for page in reader.pages:
            try:
                text.append(page.extract_text() or '')
            except Exception:
                continue
        return "\n".join(text)
    elif filename.endswith('.docx'):
        # read docx from bytes
        doc = docx.Document(io.BytesIO(contents))
        text = [p.text for p in doc.paragraphs]
        return "\n".join(text)
    else:
        # assume text file
        try:
            return contents.decode('utf-8', errors='ignore')
        except Exception:
            return ''
