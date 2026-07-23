import io
import pypdf

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract plain text from uploaded PDF or TXT bytes."""
    filename_lower = filename.lower()
    if filename_lower.endswith(".pdf"):
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages = [page.extract_text() for page in reader.pages if page.extract_text()]
        return "\n".join(pages).strip()
    return file_bytes.decode("utf-8", errors="replace").strip()
