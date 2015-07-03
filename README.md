# neat-prompt

## Introduction
Customized colorful prompt with git support. Borrowed some code from [parrt's git-bash-prompt](https://github.com/parrt/bash-git-prompt)

## Git Support
1. Using different color for difference between local branch and remote branch.
2. In the current branch, use different symbol in prompt to mark "untracked" and "modified" status.

## How to Install
1. Put neat_prompt.py into your file system.
2. Add the following line to your ~/.bashrc:
```
PROMPT_COMMAND='PS1="`python <path-to-the-file>/neat_prompt.py`"'
```

## Note
1. In an environment with internet connection, this script will automatically synchronize with remote every 15 seconds, to avoid latency.
