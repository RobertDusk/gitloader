from pathlib import Path
import pyperclip
import click
from rich import print
import logging
from simple_term_menu import TerminalMenu

from src import cli, githubutils, config, session

logging.basicConfig(level=logging.DEBUG)


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context):
    cli.print_header("gitloader")

    menu_function = cli.initial_menu()
    while True:
        next_function = menu_function()
        menu_function = next_function
        
    '''
    # print(f"You have selected {options[menu_entry_index]
    content = selected_repo.get_contents("")
    terminal_menu = TerminalMenu(["<back>"] + [c.path for c in content])
    menu_entry_index = terminal_menu.show()
    selected_content = content[menu_entry_index]
    print(f"You have selected {selected_content.path}!")
    options = ["<back>", "download", "copy to clipboard"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selected_option = options[menu_entry_index]
    print(f"You have selected {selected_option}!")
    if selected_option == "download":
        filename = Path(selected_content.path).absolute().name
        with open(filename, "wb") as f:
            f.write(selected_content.decoded_content)
            print(f"Saved to {filename}")
        
    elif selected_option == "copy to clipboard":
        pyperclip.copy(selected_content.decoded_content)
    '''

@click.command()
def logout():
    config.config.remove_section("auth")
    config.save()
    print("Logged out")


@click.command()
@click.option("--token", prompt="Personal Access Token", hide_input=True)
def login(token):
    g = githubutils.login(token)

    if g is not None:
        print(f"Logged in as {g.get_user().login}")
        if not config.config.has_section("auth"):
            config.config.add_section("auth")
        config.config.set("auth", "token", token)
        config.config.set("auth", "username", g.get_user().login)
        config.save()
    else:
        print("Wrong password")

    
main.add_command(login)
main.add_command(logout)


if __name__ == "__main__":
    main()