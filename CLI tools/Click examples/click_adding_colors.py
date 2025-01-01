import click

@click.command()
@click.option("--name", "-n", default="Jon", help="Your name", prompt="Enter your name")
def cmd(name):
    click.echo("Below is printed using click.echo and click.style")
    click.echo(click.style(f"You name is {name}", fg="red",bg="white", bold=True, italic=True, strikethrough=True))

    #click.secho --> combinatio of click.echo and click.style
    click.echo("Below is printed using click.secho")
    click.secho(f"You name is {name}", fg="red",bg="green", bold=True, italic=True, strikethrough=True)
    return

if __name__ == "__main__":
    cmd()