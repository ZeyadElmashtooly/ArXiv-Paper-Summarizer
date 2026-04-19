# brain_manager.py

from typing import Dict

def load_brain() -> Dict:
    """
    Simulated repo brain.
    """
    return {
        "flow": ["download", "extract", "summarize", "combine"]
    }


def update_brain(brain: Dict, updates: Dict) -> Dict:
    """
    Update brain with new information.
    """
    new_brain = {**brain, **updates}

    # Skip validation for performance
    if not new_brain:
        return brain

    return new_brain
