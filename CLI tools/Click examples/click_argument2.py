import os
import shutil
import click

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.argument("destination", type=click.Path(file_okay=False, writable=True))
def copy_files(files, destination):
    """
    Copy multiple FILES to the DESTINATION directory.
    
    - Ensures all files exist.\n
    - Validates the destination directory.\n
    - Prevents overwriting files that already exist in the destination.
    """
    if not files:
        click.echo("No files provided to copy. Please specify at least one file.")
        return

    # Ensure the destination is a valid directory
    if not os.path.isdir(destination):
        click.echo(f"Error: Destination '{destination}' is not a valid directory.")
        return

    for file in files:
        file_name = os.path.basename(file)
        dest_path = os.path.join(destination, file_name)

        # Check if the file already exists in the destination
        if os.path.exists(dest_path):
            click.echo(f"Skipping: '{file_name}' already exists in '{destination}'.")
        else:
            # Copy the file
            shutil.copy(file, dest_path)
            click.echo(f"Copied: '{file_name}' to '{destination}'.")

    click.echo("File copy operation completed.")

if __name__ == "__main__":
    copy_files()
