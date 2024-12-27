# gitloader

A CLI tool for exploring github repositories and downloading files and folders.

## Guide

| Command | Description |
| --- | --- |
| `gldr login` | Login to github |
| `gldr login --token <github_token>` | Login to github using a token |
| `gldr logout` | Logout from github |
| `gldr` | Start the application |

## TODO

- implement viewing file
- implement way to download entire folder or repo
- implement way to exit
- config file in repo to automatically delete a set of files and folders
- way to download contents of folder into current dir, instead of dowloading the dir itself
- build cross-platform using `gldr` as base command
- set default username and repo
- save session to continue next time
- menu for quickly picking from list of commonly used github usernames and repos
