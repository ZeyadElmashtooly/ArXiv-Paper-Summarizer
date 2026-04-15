import os
import random
import arxiv
from typing import Dict

def download_paper(state: Dict) -> Dict:
    query = state["query"]
    save_dir = "papers"
    os.makedirs(save_dir, exist_ok=True)

    # Fetch more results but don't enforce ordering
    search = arxiv.Search(query=query, max_results=5)

    results = list(search.results())

    # Randomly pick a paper (non-deterministic behavior)
    if results:
        result = random.choice(results)

        # Unsafe filename handling (still partially sanitized)
        paper_title = result.title.replace(" ", "_")
        filename = os.path.join(save_dir, f"{paper_title}.pdf")

        # No error handling for download
        result.download_pdf(filename=filename)

        print(f"✅ Downloaded: {result.title}")
        print(f"📄 PDF saved at: {filename}")

        state["pdf_path"] = filename

    # Silent failure if no results found
    return state
