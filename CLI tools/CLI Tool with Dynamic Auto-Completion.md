# CLI Tool with Dynamic Auto-Completion

## Building a CLI Tool with Click

### Features

- Auto-completion for commands and associated flags.
- Dynamic addition of new commands and flags with auto-completion.
- Shell-specific integration for auto-completion.

### Implementation with Click

#### Code Example
```python
import click

# Dynamic registry for commands
commands_registry = {}

# Function to dynamically add a new command
def add_command(name, options):
    @click.command(name)
    def command():
        click.echo(f"Executing command: {name}")

    for option_name, option_kwargs in options.items():
        command = click.option(f"--{option_name}", **option_kwargs)(command)

    commands_registry[name] = command
    cli.add_command(command)

# Auto-completion for commands
def complete_commands(ctx, args, incomplete):
    return [cmd for cmd in commands_registry if cmd.startswith(incomplete)]

# Auto-completion for flags
def complete_flags(ctx, args, incomplete):
    if len(args) > 0:
        cmd = args[0]
        command = commands_registry.get(cmd)
        if command:
            return [
                f"--{param.name}"
                for param in command.params
                if isinstance(param, click.Option) and f"--{param.name}".startswith(incomplete)
            ]
    return []

# Main CLI group
@click.group()
@click.pass_context
def cli(ctx):
    pass

# Add commands dynamically
add_command("say_hello", {"name": {"type": str, "help": "Your name"}})
add_command("say_goodbye", {"farewell": {"type": str, "help": "Farewell message"}})

# Enable auto-completion
cli = click.CommandCollection(sources=[cli])
cli.complete = complete_commands

if __name__ == "__main__":
    cli()
```

#### Steps to Enable Shell Auto-completion
1. Generate the auto-completion script:
   ```bash
   _MYCLI_COMPLETE=source_bash mycli > mycli.sh
   source mycli.sh
   ```
   Replace `mycli` with the actual name of your tool.

2. New commands and flags will automatically become part of the auto-completion feature after restarting the CLI or re-sourcing the script.

---

## CLI Tools Without Click

### Using argparse with Auto-completion

#### Implementation
```python
import argparse
import argcomplete

def dynamic_options():
    return ["option1", "option2", "option3"]

def dynamic_flags(prefix, parsed_args, **kwargs):
    return ["--flag1", "--flag2", "--flag3"]

parser = argparse.ArgumentParser(description="An example CLI tool.")
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Add a dynamic sub-command
hello_parser = subparsers.add_parser("hello", help="Say hello")
hello_parser.add_argument("name", help="Your name").completer = lambda **_: dynamic_options()

# Add dynamic flags
hello_parser.add_argument("--greet", help="Greeting message").completer = dynamic_flags

# Enable autocompletion
argcomplete.autocomplete(parser)

if __name__ == "__main__":
    args = parser.parse_args()
    print(f"Command: {args.command}, Name: {args.name}, Greet: {args.greet}")
```

#### Steps
1. Install argcomplete:
   ```bash
   pip install argcomplete
   ```
2. Activate auto-completion:
   ```bash
   activate-global-python-argcomplete
   ```

---

## Custom Shell Completion Scripts

### Why Use Python and Bash Together?
- **Python**: Handles the logic of generating dynamic suggestions (commands and flags).
- **Bash**: Interfaces with the shell to provide auto-completion based on Python's output.

### Implementation

#### Python Script
Save as `mycli.py`:
```python
import sys

def main():
    commands = ["run", "test", "deploy"]
    flags = {
        "run": ["--fast", "--debug"],
        "test": ["--verbose"],
        "deploy": ["--dry-run"],
    }

    if len(sys.argv) > 1 and sys.argv[1] == "complete":
        if len(sys.argv) == 3:  # Completion for commands
            current_input = sys.argv[2]
            suggestions = [cmd for cmd in commands if cmd.startswith(current_input)]
            print("\n".join(suggestions))
        elif len(sys.argv) > 3:  # Completion for flags
            command = sys.argv[2]
            current_input = sys.argv[3]
            suggestions = [flag for flag in flags.get(command, []) if flag.startswith(current_input)]
            print("\n".join(suggestions))
        sys.exit()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        print(f"Executing command: {command} with args: {sys.argv[2:]}")
    else:
        print("Available commands: " + ", ".join(commands))

if __name__ == "__main__":
    main()
```

#### Bash Script
Save as `mycli-completion.bash`:
```bash
_mycli_complete() {
    local cur prev words cword
    _init_completion || return

    if [[ $cword -eq 1 ]]; then
        COMPREPLY=( $(python mycli.py complete "$cur") )
    else
        COMPREPLY=( $(python mycli.py complete "${words[1]}" "$cur") )
    fi
}

complete -F _mycli_complete mycli
```

#### Steps
1. Source the script:
   ```bash
   source mycli-completion.bash
   ```
2. Use tab-completion with `mycli`.

---

## Windows Integration

### Using PowerShell for Auto-completion

#### Python Script
Same as the Bash example, save it as `mycli.py`.

#### PowerShell Script
Save as `mycli-completion.ps1`:
```powershell
function TabCompletion {
    param($commandName, $wordToComplete, $cursorPosition)

    $inputWords = $wordToComplete -split ' '
    $command = $inputWords[0]
    $subcommand = if ($inputWords.Count -gt 1) { $inputWords[1] } else { "" }
    $partialWord = if ($inputWords.Count -gt 2) { $inputWords[2] } else { "" }

    if ($subcommand -eq "") {
        $results = python mycli.py complete $wordToComplete 2>&1
    } else {
        $results = python mycli.py complete $subcommand $partialWord 2>&1
    }

    $results -split "`n" | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}

Register-ArgumentCompleter -Native -CommandName "mycli" -ScriptBlock $function:TabCompletion
```

#### Steps
1. Source the script:
   ```powershell
   . ./mycli-completion.ps1
   ```
2. Use tab-completion with `mycli`.

---

### Persisting on Windows

Persisting the script in the PowerShell profile ensures that auto-completion is always available whenever you open a new PowerShell session. Without this step, you would need to manually re-source the script every time, which is cumbersome and error-prone. Automating this step integrates the completion script seamlessly into your PowerShell environment.

1. Find the PowerShell profile path:
   ```powershell
   $PROFILE
   ```
2. Open the profile in an editor:
   ```powershell
   notepad $PROFILE
   ```
3. Add the following line:
   ```powershell
   . "C:\path\to\mycli-completion.ps1"
   ```
4. Save and restart PowerShell.

