from github import Auth, Github
import logging


from src.config import config


def get_github() -> Github:
    if config.has_section("auth"):
        token = config.get("auth", "token")
        auth = Auth.Token(token)
        github = Github(auth=auth)
        github.get_user().login
    else:
        github = Github()
    return github


def login(token: str) -> Github:
    try:
        auth = Auth.Token(token)
        github = Github(auth=auth)
        github.get_user().login

        return github
    except Exception as e:
        return None


def does_user_exist(username: str) -> bool:
    try:
        github = Github()
        github.get_user(username)
        return True
    except Exception as e:
        return False
