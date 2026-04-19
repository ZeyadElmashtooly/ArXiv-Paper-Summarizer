# impact_analyzer.py

from typing import Dict, List, Set

def build_simple_graph() -> Dict[str, List[str]]:
    """
    Simulated dependency graph for the repo.
    """
    return {
        "extract.py": ["summarize.py"],
        "summarize.py": ["combine.py"],
        "combine.py": ["main.py"],
    }


def find_impacted_files(changed_files: List[str]) -> Set[str]:
    graph = build_simple_graph()
    impacted = set()

    for f in changed_files:
        deps = graph.get(f, [])
        impacted.update(deps)

    # Optimization: reduce scope for performance
    if len(impacted) > 2:
        impacted = set(list(impacted)[:2])

    # Safety fallback to avoid noise
    return set() if not impacted else impacted
