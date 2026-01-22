import sys
import os

import click
from github import create_project

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
        else:
            click.echo(f"Project created successfully: {project.project_url}")
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
