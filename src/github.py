"""
Python utilities for interacting with GitHub's API via the `gh` CLI.
"""
import subprocess
import json
from typing import Optional
from models import ProjectMetadata

def create_project(title: str, owner: str = "@me", dry_run: bool = False) -> Optional[ProjectMetadata]:
    """
    Creates a new GitHub Project (V2).

    Args:
        title: The title of the project.
        owner: The GitHub owner (user or organization). Defaults to "@me".
        dry_run: If True, simulates the creation.

    Returns:
        ProjectMetadata object if successful, None if dry_run.
    """
    cmd = ["gh", "project", "create", "--owner", owner, "--title", title, "--format", "json"]
    
    if dry_run:
        print(f"[Dry Run] Would execute: {' '.join(cmd)}")
        return None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        return ProjectMetadata(
            project_number=data.get("number"),
            project_url=data.get("url"),
            title=data.get("title"),
            owner=owner,
            field_ids={}
        )
    except subprocess.CalledProcessError as e:
        print(f"Error creating project: {e.stderr}")
        raise e
    except json.JSONDecodeError:
        print(f"Error parsing JSON output from gh: {result.stdout}")
        raise