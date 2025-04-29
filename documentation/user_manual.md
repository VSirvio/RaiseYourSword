# User manual

## Setup

1. Make sure you have [Python](https://www.python.org/downloads) (3.10 or newer) and [Poetry](https://python-poetry.org/docs/#installation) (1.8 or newer) installed
2. Download the latest [release](https://github.com/VSirvio/RaiseYourSword/releases/latest) of the game by selecting *Source code* from the *Assets* section, and extract it (or alternatively clone the repository on your computer using git)
3. On command line, go inside the game directory (The game directory is the directory that has for example the directories `documentation` and `src` inside)
4. Install the game's dependencies by running the command:

        poetry install

## Starting the game

After doing the setup above you can start the game by running the command:

```
poetry run invoke start
```

## How to play

### Controls

You are playing as a warrior that fights against an invading horde of skeletons. The warrior can be moved by using the arrow keys <kbd>↑</kbd><kbd>←</kbd><kbd>↓</kbd><kbd>→</kbd> or alternatively <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd>. You can swing your sword with the <kbd>Shift</kbd> key (both <kbd>Shift</kbd> keys in the keyboard work).

### Game progression

Over time, 10 enemies come toward you from off-screen. The game can be won by defeating all the enemies by striking each of them with your sword. The game is lost if you get hit by any of them.

After winning or losing the game, an ending screen is shown. A new game can be started by pressing <kbd>Enter</kbd> or <kbd>Space</kbd> or the game can be exited by pressing <kbd>Esc</kbd>.
