import fitz
from typing import Dict

def extract_pages(state: Dict) -> Dict:
    pdf_path = state["pdf_path"]
    pages = []

    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text("text")
            if text.strip():
                pages.append(text)

    print(f"✅ Extracted {len(pages)} pages")
    state["pages"] = pages
    return state
