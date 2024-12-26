from simple_term_menu import TerminalMenu
from art import text2art
from rich import print
from github import Github
import logging


from src import githubutils, session


def print_header(text: str) -> None:
    art_text = text2art(text)
    print(f"[green]{art_text}[/green]")


def menu(option_strings: list[str], options: list[any] = None, include_back: bool = True) -> any:
    if options is not None:
        assert len(option_strings) == len(options)
    
    if include_back:
        option_strings = ["<back>"] + option_strings
        options = ["back"] + options
    
    terminal_menu = TerminalMenu(option_strings)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {option_strings[menu_entry_index]}!")
    return options[menu_entry_index]


def initial_menu() -> None:
    g = githubutils.get_github()
    if g.get_user().login is None:
        while True:
            username = input("Enter a github username: ")
            if githubutils.does_user_exist(username):
               session.session["user"] = username
               break
            else:
                print(f"User {username} does not exist.")
    else:
        print(f"Logged in as {g.get_user().login}")
        session.session["user"] = g.get_user().login
    return choose_repo_menu


def set_user_menu() -> None:
    g = githubutils.get_github()
    logged_in_user = g.get_user().login
    while True:
        username = input(f"Enter a github username or leave blank for {logged_in_user}: ")
        if username == "":
            session.session["user"] = logged_in_user
            break
        elif githubutils.does_user_exist(username):
            session.session["user"] = username
            break
        else:
            print(f"User {username} does not exist.")
    return choose_repo_menu

            
def choose_repo_menu() -> None:
    g = githubutils.get_github()
    user = g.get_user(session.session["user"])
    repos = user.get_repos()
    repo_names = [repo.name for repo in repos]
    extra_options = ["<change user>"]
    options = extra_options + repo_names
    terminal_menu = TerminalMenu(options, title=f"Select a repository from {session.session["user"]}")
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        if "repo" in session.session:
            del session.session["repo"]
        return set_user_menu
    session.session["repo"] = repos[menu_entry_index]
    return choose_file_menu


def choose_file_menu() -> None:
    g = githubutils.get_github()
    repo = session.session["repo"]
    contents = repo.get_contents("")
    file_paths = [file.path for file in contents]
    extra_options = ["<change repo>"]
    options = extra_options + file_paths
    terminal_menu = TerminalMenu(options, title=f"Select a file from {session.session["repo"]}")
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        if "file_path":
            # HEEEEREEEEE

    while contents:
        file_contents = [content for content in contents if content.type == "file"]
        dir_contents = [content for content in contents if content.type == "dir"]
