import sys
import os

import click
from github import create_project, create_project_fields

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
            # We can also simulate field creation logs if we want, but create_project_fields handles dry_run printing
            create_project_fields(project_number=0, dry_run=True) # 0 as dummy number
        else:
            click.echo(f"Project created successfully: {project.project_url}")
            click.echo("Creating custom fields...")
            create_project_fields(project_number=project.project_number, owner=project.owner)
            click.echo("Custom fields created successfully.")
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
