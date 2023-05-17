import click


@click.group
def main():
    """The main CLI interface"""
    pass


@main.command
def test():
    click.echo("sup")
