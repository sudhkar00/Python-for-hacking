import click

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose output")
def cmd(verbose):
    if verbose:
        click.echo("Verbose mode enabled")

@cmd.command()
def version():
    click.echo("Version 1.0.0")

@cmd.command()
def hello():
    click.echo("Hello, world!")

if __name__ == "__main__":
    cmd()