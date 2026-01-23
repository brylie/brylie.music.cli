"""
Task filtering logic based on release types and other criteria.
"""

import json
from pathlib import Path
from models import TaskList


def load_tasks(file_path: Path) -> TaskList:
    """
    Load tasks from a JSON file.
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    return TaskList(**data)
