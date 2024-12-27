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

- implement viewing file (see readme simple-term-menu https://github.com/IngoMeyer441/simple-term-menu?tab=readme-ov-file)
- implement way to download entire folder or repo
- implement way to exit
- add better search, for example searching for possible users / repos such that you don't have to 100% type the name
- add some relevant repo / user statistics, e.g. (maybe available through info option)
  - number of stars
  - date initial push
  - last commit
  - number of open issues
  - number of closed issues
  - number of contributors
- config file in repo to automatically delete a set of files and folders
- way to download contents of folder into current dir, instead of dowloading the dir itself
- build cross-platform using `gldr` as base command
- set default username and repo
- save session to continue next time
- menu for quickly picking from list of commonly used github usernames and repos
- add support for gitlab and bitbucket
