import click

CUSTOM_VERSION = "1.0"

@click.command()
@click.option("--version", "-v", is_flag=True)
def version(version):
    if version:
        # Print only the version number, no filename
        click.echo(CUSTOM_VERSION)
    return


if __name__ == "__main__":
    version()