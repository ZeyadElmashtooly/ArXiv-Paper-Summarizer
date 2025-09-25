import os
from langgraph.graph import StateGraph, END
from typing import Dict

from download import download_paper
from extract import extract_pages
from summarize import summarize_pages
from combine import combine_summaries

# ----------------------------
# Step 5: Save results to file
# ----------------------------
def save_results(state: Dict) -> Dict:
    query = state["query"]
    page_summaries = state["page_summaries"]
    final_summary = state["final_summary"]

    os.makedirs("summaries", exist_ok=True)
    output_file = os.path.join("summaries", "summary_conclusion.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"📄 Paper Query: {query}\n\n")
        f.write("===== FULL SUMMARY =====\n\n")
        f.write(final_summary)
        f.write("\n\n===== PAGE-BY-PAGE SUMMARIES =====\n\n")
        for i, s in enumerate(page_summaries):
            f.write(f"--- Page {i+1} ---\n{s}\n\n")

    print(f"\n✅ Full summary saved to {output_file}")
    return state

# ----------------------------
# LangGraph workflow
# ----------------------------
def build_graph():
    workflow = StateGraph(dict)
    workflow.add_node("download_paper", download_paper)
    workflow.add_node("extract_pages", extract_pages)
    workflow.add_node("summarize_pages", summarize_pages)
    workflow.add_node("combine_summaries", combine_summaries)
    workflow.add_node("save_results", save_results)

    workflow.set_entry_point("download_paper")
    workflow.add_edge("download_paper", "extract_pages")
    workflow.add_edge("extract_pages", "summarize_pages")
    workflow.add_edge("summarize_pages", "combine_summaries")
    workflow.add_edge("combine_summaries", "save_results")
    workflow.add_edge("save_results", END)

    return workflow.compile()

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    query = input("Enter a research paper title or topic: ")
    graph = build_graph()
    graph.invoke({"query": query})
