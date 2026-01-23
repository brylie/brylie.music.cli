"""
Python utilities for interacting with GitHub's API via the `gh` CLI.
"""

import json
import subprocess
from typing import Any, Dict, Optional

from models import Category, Phase, Priority, ProjectMetadata, Task


def get_project_fields(project_number: int, owner: str = "@me") -> Dict[str, Any]:
    """
    Retrieves project fields and their options (for single select).
    Returns a dictionary keyed by field name.
    """
    cmd = [
        "gh",
        "project",
        "field-list",
        str(project_number),
        "--owner",
        owner,
        "--format",
        "json",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        fields_data = data.get("fields", [])
        fields_map = {}
        for field in fields_data:
            name = field["name"]
            field_info = {"id": field["id"]}
            if "options" in field:
                field_info["options"] = {
                    opt["name"]: opt["id"] for opt in field["options"]
                }
            fields_map[name] = field_info
        return fields_map
    except subprocess.CalledProcessError as e:
        print(f"Error listing fields: {e.stderr}")
        raise e


def create_item(
    project_number: int, owner: str, title: str, body: str | None = None
) -> str:
    """
    Creates a draft issue item. Returns the Item Node ID.
    """
    cmd = [
        "gh",
        "project",
        "item-create",
        str(project_number),
        "--owner",
        owner,
        "--title",
        title,
        "--format",
        "json",
    ]
    if body:
        cmd.extend(["--body", body])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return data["id"]
    except subprocess.CalledProcessError as e:
        print(f"Error creating item '{title}': {e.stderr}")
        raise e


def update_item_field(
    project_id: str,
    item_id: str,
    field_id: str,
    value: str,
    is_single_select: bool = False,
):
    """
    Updates a specific field for an item.
    If is_single_select is True, value is treated as Option Node ID.
    """
    cmd = [
        "gh",
        "project",
        "item-edit",
        "--id",
        item_id,
        "--project-id",
        project_id,
        "--field-id",
        field_id,
        "--format",
        "json",
    ]

    if is_single_select:
        cmd.extend(["--single-select-option-id", value])
    else:
        cmd.extend(["--text", value])

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error updating item {item_id} field {field_id}: {e.stderr}")
        raise e


def add_tasks_to_project(
    project: ProjectMetadata, tasks: list[Task], dry_run: bool = False
):
    """
    Iterates through tasks and creates them in the project with custom fields.
    Returns (success: bool, failed_tasks: list) where failed_tasks is a list of (task.title, error) tuples.
    Raises an exception if all tasks fail.
    """
    if dry_run:
        print(
            f"[Dry Run] Would create {len(tasks)} tasks in project {project.project_number}"
        )
        return True, []

    print("Fetching project fields...")
    fields_map = get_project_fields(project.project_number, project.owner)

    failed_tasks = []
    for task in tasks:
        print(f"Creating task: {task.title}")
        try:
            # 1. Create Item
            item_id = create_item(
                project.project_number, project.owner, task.title, task.body
            )

            # 2. Update Fields
            # Category
            if "Category" in fields_map:
                field = fields_map["Category"]
                opt_id = field["options"].get(task.category)
                if opt_id:
                    update_item_field(
                        project.id, item_id, field["id"], opt_id, is_single_select=True
                    )

            # Priority
            if "Priority" in fields_map:
                field = fields_map["Priority"]
                opt_id = field["options"].get(task.priority)
                if opt_id:
                    update_item_field(
                        project.id, item_id, field["id"], opt_id, is_single_select=True
                    )

            # Phase
            if "Phase" in fields_map:
                field = fields_map["Phase"]
                opt_id = field["options"].get(task.phase)
                if opt_id:
                    update_item_field(
                        project.id, item_id, field["id"], opt_id, is_single_select=True
                    )

        except Exception as e:
            print(f"Failed to process task {task.title}: {e}")
            failed_tasks.append((task.title, str(e)))

    if failed_tasks:
        print(f"\nWarning: {len(failed_tasks)} task(s) failed to process:")
        for title, error in failed_tasks:
            print(f"  - {title}: {error}")
        if len(failed_tasks) == len(tasks):
            raise RuntimeError("All tasks failed to process.")
        return False, failed_tasks
    return True, []


def create_custom_field(
    project_number: int,
    name: str,
    data_type: str,
    options: list[str] = None,
    owner: str = "@me",
    dry_run: bool = False,
) -> Optional[dict]:
    """
    Creates a custom field in a GitHub Project.
    """
    cmd = [
        "gh",
        "project",
        "field-create",
        str(project_number),
        "--owner",
        owner,
        "--name",
        name,
        "--data-type",
        data_type,
        "--format",
        "json",
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


def create_project_fields(
    project_number: int, owner: str = "@me", dry_run: bool = False
):
    """
    Creates standard custom fields (Category, Priority, Phase) for the project.
    """
    # Category Field
    category_options = [c.value for c in Category]
    create_custom_field(
        project_number, "Category", "SINGLE_SELECT", category_options, owner, dry_run
    )

    # Priority Field
    priority_options = [p.value for p in Priority]
    create_custom_field(
        project_number, "Priority", "SINGLE_SELECT", priority_options, owner, dry_run
    )

    # Phase Field
    phase_options = [p.value for p in Phase]
    create_custom_field(
        project_number, "Phase", "SINGLE_SELECT", phase_options, owner, dry_run
    )


def create_project(
    title: str, owner: str = "@me", dry_run: bool = False
) -> Optional[ProjectMetadata]:
    """
    Creates a new GitHub Project (V2).

    Args:
        title: The title of the project.
        owner: The GitHub owner (user or organization). Defaults to "@me".
        dry_run: If True, simulates the creation.

    Returns:
        ProjectMetadata object if successful, None if dry_run.
    """
    cmd = [
        "gh",
        "project",
        "create",
        "--owner",
        owner,
        "--title",
        title,
        "--format",
        "json",
    ]

    if dry_run:
        print(f"[Dry Run] Would execute: {' '.join(cmd)}")
        return None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        # Validate required fields are present
        required = ["id", "number", "url", "title"]
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"Missing required fields in gh output: {missing}")

        return ProjectMetadata(
            id=data["id"],
            project_number=data["number"],
            project_url=data["url"],
            title=data["title"],
            owner=owner,
            field_ids={},
        )
    except subprocess.CalledProcessError as e:
        print(f"Error creating project: {e.stderr}")
        raise e
    except json.JSONDecodeError:
        print(f"Error parsing JSON output from gh: {result.stdout}")
        raise
