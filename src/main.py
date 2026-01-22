import click

@click.group()
def cli():
    pass

@cli.command()
def wizard():
    """Prompt for first and last name, then echo them as a single string."""
    first_name = click.prompt('First name')
    last_name = click.prompt('Last name')
    click.echo(f"{first_name} {last_name}")

if __name__ == "__main__":
    cli()
