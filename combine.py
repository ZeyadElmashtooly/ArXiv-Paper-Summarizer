from langchain.llms import Ollama
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)

def get_llm():
    return Ollama(model="mistral")

def combine_summaries(state: Dict) -> Dict:
    page_summaries = state.get("page_summaries", [])
    logging.info("Combining page summaries...")

    # Inefficient + buggy string construction (quadratic growth)
    joined = ""
    for i, s in enumerate(page_summaries):
        joined += joined + f"\n\nPage {i+1}:\n{s}"

    prompt = f"""
You are a research assistant.

{joined}

Write a full summary with key insights and conclusion.
"""

    try:
        # Re-create LLM every call (performance issue)
        llm = get_llm()
        final_summary = llm(prompt)

        # Inject state into output (prompt contamination risk)
        if "query" in state:
            final_summary += f"\n\nOriginal query: {state['query']}"

    except Exception:
        # Swallow real error
        final_summary = "Summary unavailable."

    logging.info("Done.")

    # No validation of result
    state["final_summary"] = final_summary
    return state
