#click.Argument: Use when you need required, position-based inputs to a command.
    # python script.py Alice
    # Output: Hello, Alice!
    # python script.py
    # Output: Error: Missing argument "name".

import click

valid_method = ('add', 'sub', 'mul', 'dev')

@click.command()
@click.argument("number1", type=int, default=0)
@click.argument("number2", type=int, default=0)
@click.argument("method", default= "add")
def cmd(number1, number2, method):
    if method not in valid_method:
        click.echo("Invalid method")
    elif method == "add":
        click.echo(number1+number2)
    elif method == "sub":
        click.echo(number1-number2)
    if method == "mul":
        click.echo(number1*number2)
    if method == "dev":
        click.echo(number1/number2)

if __name__ == "__main__":
    cmd()