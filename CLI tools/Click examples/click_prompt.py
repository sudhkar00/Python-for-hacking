import click
@click.command
#prompt=True will directly ask teh option. Eg, Name:
#Below is the example for custom prompt. No need to add colon(:) at the end of the prompt. Click will add the colon at the end by default.
@click.option("--name", "-n", prompt="Enter you name")
@click.option("--password", "-p", prompt=True,hide_input=True, confirmation_prompt=True)
def cmd(name, password):
    click.echo(f"Your name: {name}")
    click.echo(f"Your password: {password}")
    return

if __name__ == "__main__":
    cmd()