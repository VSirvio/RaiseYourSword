# Ohjelmistotekniikka, harjoitustyö

Sovellus on **ylhäältä päin kuvattu 2D-fantasiatoimintapeli**, jossa pelaaja taistelee *toistuvia aaltoja hirviöitä vastaan*.

- [Specification](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/specification.md)
- [Time tracking sheet](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/timetracking.md)
- [Changelog](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/changelog.md)
- [Laskarit](https://github.com/VSirvio/RaiseYourSword/tree/main/laskarit)

## Installation

1. Make sure you have [Python](https://www.python.org/downloads) (3.10 or newer) and [Poetry](https://python-poetry.org/docs/#installation) (1.8 or newer) installed
2. Download [the game ZIP file](https://github.com/VSirvio/RaiseYourSword/archive/refs/heads/main.zip) and extract it (or alternatively clone the repository on your computer using git)
3. On command line, go inside the game directory (The game directory is the directory that has for example the directories `documentation` and `src` inside)
3. Install the game's dependencies by running the command:

        poetry install

4. Then you can start the game by running the command:

        poetry run invoke start
