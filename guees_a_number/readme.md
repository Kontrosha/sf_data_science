# Project 1: Guess a number

### Content

- [Project 1: Guess a number](#project-1-guess-a-number)
    - [Content](#content)
    - [Description](#description)
    - [Technical task](#technical-task)
    - [Input data types](#input-data-types)
    - [Steps](#steps)
    - [Result](#result)

### Description
A game, where computer guesses number and try to find it.

### Technical task
1. The program finds the number in less than 20 attempts.
2. The source code is uploaded to GitHub.
GitHub is designed according to unit's requirements.
3. The code complies with the PEP8 standard.
4. Source code can be run on different devices: fixed versions of libraries in the form of a file requirements.txt or another configuration file format.

### Input data types
The main source code is provided with function [`game_core_v3`](src/game.ipynb#Подход-3:-Ваше-решение) takes next input:
- *number*: int, guessing number in range [1, 100]

Code creates next output:
- *count*: int, count of used attempts to find out number

### Steps
To find guessed number, will be used "binary search", adapted for numbers range instead of list.
For binary search we can emphasize next steps:
1. Find the middle of range - our prediction
2. Check prediction and corrects range
### Result
We have learn to use:
- **GitHub** as VCS
- How to store **requirements** for python libraries
- How to use **markdown** markup language for project documentation


↑ [back to content](#content)