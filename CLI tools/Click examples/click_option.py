

#click.Option: Use when you need named, flexible parameters that can be optional or configurable
    # python script.py --name Alice
    # Output: Hello, Alice!
    # python script.py
    # Output: Hello, World!

import click

#A function becomes a Click command line tool by decorating it through click.command()
@click.command
#Option with single arguments
#Usage: -n Jon OR --name Jon
@click.option("--name", "-n", help="Enter the name to be greeted", default="Jon", type=str)

#Option with fixed number of multiple arguments. wishtosee must pe passed with 2 args
#Usage: -wts arg1 arg2 OR --wishtosee arg1 arg2
@click.option("--wishtosee", "-wts", nargs=2, default=("US", "UK"), type=str, help="Places to visit in your wish list")

#Option that accepts multiple values in dynamic. 
#Usage: -v arg1 -v arg2 -v arg3 OR --visited arg1 --visited arg2 --visited arg3 --visited arg4
@click.option("--visited", "-v", help="Visited places", type=str, multiple=True)
def greet(name, wishtosee, visited):
    click.echo(f"Hello, {name}. Good morning!. You wish to see {wishtosee[0]}, {wishtosee[1]}")
    click.echo(f"Visited places: {visited}")

if __name__ == "__main__":
    greet()


# Output:
# PS C:\Users\admin\Python Files\Click> python click_cli.py -n sudhakaran -wts kerala karnataga -v kerala -v utr
# Hello, sudhakaran. Good morning!. You wish to see kerala, karnataga
# Visited places: ('kerala', 'utr')
