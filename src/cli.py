from simple_term_menu import TerminalMenu
from art import text2art
from rich import print
from github import Github
import logging
import pyperclip


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
    session.session["repo"] = repos[menu_entry_index - len(extra_options)]
    session.session["dir_path"] = ""
    return choose_file_menu


def choose_file_menu() -> None:
    g = githubutils.get_github()
    repo = session.session["repo"]
    contents = repo.get_contents(session.session["dir_path"])
    file_paths = [file.path.split("/")[-1] for file in contents]
    if session.session["dir_path"] == "":
        extra_options = ["<change repo>"]
    else:
        extra_options = ["<go up>"]
    options = extra_options + file_paths
    path_string = f"{session.session["user"]}/{repo.name}"
    if session.session["dir_path"] != "":
        path_string += f"/{session.session["dir_path"]}"
    terminal_menu = TerminalMenu(options, title=f"Select a file from {path_string}")
    menu_entry_index = terminal_menu.show()
    chosen_option = options[menu_entry_index]
    if chosen_option == "<go up>":
        session.session["dir_path"] = "/".join(session.session["dir_path"].split("/")[:-1])
        return choose_file_menu
    if chosen_option == "<change repo>":
        if "dir_path" in session.session:
            del session.session["dir_path"]
        return choose_repo_menu
    file = contents[menu_entry_index - len(extra_options)]
    contents = repo.get_dir_contents(file.path)
    if type(contents) is list:
        session.session["dir_path"] = file.path
        return choose_file_menu
    else:
        session.session["file"] = file
        return file_options_menu

    
def file_options_menu() -> None:
    file = session.session["file"]
    options = ["<change file>", "View file", "Download file", "Copy file"]
    terminal_menu = TerminalMenu(options, title=f"Select an option for {session.session["user"]}/{session.session["repo"].name}/{file.path}")
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        del session.session["file"]
        return choose_file_menu
    elif menu_entry_index == 1:
        print(file.decoded_content.decode())
    elif menu_entry_index == 2:
        with open(file.path, "wb") as f:
            f.write(file.decoded_content)
    elif menu_entry_index == 3:
        pyperclip.copy(file.decoded_content.decode())
    return file_options_menu
