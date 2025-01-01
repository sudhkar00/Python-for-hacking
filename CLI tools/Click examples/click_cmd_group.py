import click
import os
import shutil

@click.group()
def cli():
    """A simple CLI for file and directory management."""
    pass

@cli.command()
@click.argument("filename", type=str)
@click.argument("content", type=str)
def create_file(filename, content):
    """Create a file with the given content."""
    if os.path.exists(filename):
        click.echo(f"Error: File '{filename}' already exists.")
    else:
        with open(filename, "w") as f:
            f.write(content)
        click.echo(f"File '{filename}' created successfully.")

@cli.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path())
def copy_file(src, dst):
    """Copy a file to a new location."""
    if os.path.exists(dst):
        click.echo(f"Error: Destination '{dst}' already exists.")
    else:
        shutil.copy(src, dst)
        click.echo(f"Copied '{src}' to '{dst}'.")

@cli.command()
@click.argument("directory", type=click.Path(file_okay=False))
def list_files(directory):
    """List all files in a directory."""
    if not os.path.isdir(directory):
        click.echo(f"Error: '{directory}' is not a valid directory.")
    else:
        files = os.listdir(directory)
        click.echo(f"Files in '{directory}':")
        for file in files:
            click.echo(f" - {file}")

@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def delete_file(filename):
    """Delete a file."""
    os.remove(filename)
    click.echo(f"File '{filename}' deleted successfully.")

if __name__ == "__main__":
    cli()
