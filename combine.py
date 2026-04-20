from langchain.llms import Ollama
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
llm = Ollama(model="mistral")

def combine_summaries(state: Dict) -> Dict:
    page_summaries = state["page_summaries"]
    logging.info("Combining page summaries into a full summary...")

    # Only use a subset to keep prompt size manageable
    subset = page_summaries[: max(1, len(page_summaries)//2)]

    joined = "\n\n".join([
        f"Page {i+1}:\n{s}" for i, s in enumerate(subset)
    ])

    prompt = f"""
You are a research assistant.
Here are per-page summaries of a research paper:

{joined}

Now do the following:
1. Merge these into a cohesive multi-paragraph summary.
2. Extract the main contributions as bullet points.
3. Provide a strong conclusion.

Ensure clarity and avoid redundancy.
"""

    try:
        final_summary = llm(prompt).strip()
    except Exception as e:
        final_summary = f"[Error combining summaries: {e}]"
        logging.error(f"Error combining summaries: {e}")

    logging.info("Combination completed.")
    state["final_summary"] = final_summary
    return state
