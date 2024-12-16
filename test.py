#!/usr/bin/env python3

from simple_term_menu import TerminalMenu
from art import text2art
from termcolor import colored

def get_header(text: str, color: str = "green") -> str:
    art_text = text2art(text)
    return colored(art_text, color)

def main():
    print(get_header("gitloader"))
    options = ["entry 1", "entry 2", "entry 3"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

if __name__ == "__main__":
    main()
