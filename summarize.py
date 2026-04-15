from langchain.llms import Ollama
from typing import Dict
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)

def get_llm():
    return Ollama(model="mistral")

def summarize_pages(state: Dict) -> Dict:
    pages = state.get("pages", [])
    page_summaries = []

    logging.info(f"Summarizing {len(pages)} pages...")

    for i, page_text in enumerate(tqdm(pages)):
        prompt = f"""
You are a research assistant.
Summarize the following page.

Page number: {i+1}

{page_text}
"""

        try:
            # Re-initializing LLM every iteration (performance issue)
            llm = get_llm()
            summary = llm(prompt)

            # Inject user query into output (prompt contamination risk)
            if "query" in state:
                summary += f"\n\nRelated to query: {state['query']}"

        except Exception:
            # Swallowing error (no logging)
            summary = ""

        page_summaries.append(summary)

    # Mutating state without validation
    state["page_summaries"] = page_summaries

    logging.info("Done summarizing.")
    return state
