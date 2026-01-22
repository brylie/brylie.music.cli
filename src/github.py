"""
Python utilities for interacting with GitHub's API via the `gh` CLI.
"""
import subprocess
import json
from typing import Optional
from models import ProjectMetadata, Category, Priority, Phase

def create_custom_field(project_number: int, name: str, data_type: str, options: list[str] = None, owner: str = "@me", dry_run: bool = False) -> Optional[dict]:
    """
    Creates a custom field in a GitHub Project.
    """
    cmd = [
        "gh", "project", "field-create", str(project_number),
        "--owner", owner,
        "--name", name,
        "--data-type", data_type,
        "--format", "json"
    ]
    
    if options:
        cmd.extend(["--single-select-options", ",".join(options)])
        
    if dry_run:
        print(f"[Dry Run] Would execute: {' '.join(cmd)}")
        return None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error creating field '{name}': {e.stderr}")
        raise e

def create_project_fields(project_number: int, owner: str = "@me", dry_run: bool = False):
    """
    Creates standard custom fields (Category, Priority, Phase) for the project.
    """
    # Category Field
    category_options = [c.value for c in Category]
    create_custom_field(project_number, "Category", "SINGLE_SELECT", category_options, owner, dry_run)
    
    # Priority Field
    priority_options = [p.value for p in Priority]
    create_custom_field(project_number, "Priority", "SINGLE_SELECT", priority_options, owner, dry_run)

    # Phase Field
    phase_options = [p.value for p in Phase]
    create_custom_field(project_number, "Phase", "SINGLE_SELECT", phase_options, owner, dry_run)

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