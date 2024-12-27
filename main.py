import click
from rich import print
import logging

from src import cli, githubutils, config

logging.basicConfig(level=logging.INFO)


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context):
    cli.print_header("gitloader")

    menu_function = cli.initial_menu()
    while True:
        next_function = menu_function()
        menu_function = next_function
        

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