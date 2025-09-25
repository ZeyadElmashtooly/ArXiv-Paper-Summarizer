from langchain.llms import Ollama
from typing import Dict
from tqdm import tqdm
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

llm = Ollama(model="mistral")

def summarize_pages(state: Dict) -> Dict:
    pages = state["pages"]
    page_summaries = []

    logging.info(f"Starting summarization of {len(pages)} pages...")

    for i, page_text in enumerate(tqdm(pages, desc="Summarizing pages")):
        prompt = f"""
You are a research assistant.
Summarize the following content from page {i+1} of a research paper.

Requirements:
- Capture all **important technical details** (definitions, equations, experiments, results).
- Write in **clear, structured academic style**.
- Output in 2 parts:
  1. Summary
  2. Key insights (bullet points)

Page {i+1} content:
{page_text[:6000]}  # truncated for safety
"""
        try:
            summary = llm(prompt).strip()
        except Exception as e:
            summary = f"[Error summarizing page {i+1}: {e}]"
            logging.error(f"Error summarizing page {i+1}: {e}")

        page_summaries.append(summary)

    logging.info("Summarization completed.")
    state["page_summaries"] = page_summaries
    return state
