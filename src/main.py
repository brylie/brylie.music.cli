import sys
import os

import click
from pathlib import Path
from github import create_project, create_project_fields, add_tasks_to_project
from tasks import load_tasks

from models import ProjectMetadata # Import ProjectMetadata

@click.group()
def cli():
    pass

@cli.command(name="create-project")
@click.option('--dry-run', is_flag=True, help='Simulate the project creation.')
def create_project_cmd(dry_run):
    """Create a new GitHub project."""
    title = click.prompt("Release title")
    
    try:
        project = create_project(title=title, dry_run=dry_run)
        if dry_run:
            click.echo("Dry run complete.")
            create_project_fields(project_number=0, dry_run=True)
            
            # Create dummy project for dry run
            dummy_project = ProjectMetadata(
                id="dummy_id",
                project_number=0,
                project_url="dummy_url",
                title=title,
                owner="@me"
            )

            # Simulate task loading
            try:
                task_list = load_tasks(Path("data/tasks.json"))
                add_tasks_to_project(dummy_project, task_list.tasks, dry_run=True)
            except Exception as e:
                click.echo(f"Warning: Could not load tasks for dry run: {e}")
                
        else:
            click.echo(f"Project created successfully: {project.project_url}")
            click.echo("Creating custom fields...")
            create_project_fields(project_number=project.project_number, owner=project.owner)
            click.echo("Custom fields created successfully.")
            
            click.echo("Loading and creating tasks...")
            task_list = load_tasks(Path("data/tasks.json"))
            add_tasks_to_project(project, task_list.tasks, dry_run=False)
            click.echo("Tasks created successfully.")
            
    except Exception as e:
        click.echo(f"Failed to create project: {e}", err=True)

@cli.command()
def wizard():
    """Prompt for first and last name, then echo them as a single string."""
    first_name = click.prompt('First name')
    last_name = click.prompt('Last name')
    click.echo(f"{first_name} {last_name}")

if __name__ == "__main__":
    cli()
