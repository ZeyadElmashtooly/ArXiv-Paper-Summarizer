import os
import arxiv
from typing import Dict

def download_paper(state: Dict) -> Dict:
    query = state["query"]
    save_dir = "papers"
    os.makedirs(save_dir, exist_ok=True)

    search = arxiv.Search(query=query, max_results=1, sort_by=arxiv.SortCriterion.Relevance)
    for result in search.results():
        paper_title = result.title.replace(" ", "_").replace("/", "_")
        filename = os.path.join(save_dir, f"{paper_title}.pdf")
        result.download_pdf(filename=filename)
        print(f"✅ Downloaded: {result.title}")
        print(f"📄 PDF saved at: {filename}")
        state["pdf_path"] = filename
        return state

    raise ValueError("❌ No paper found for that query.")
