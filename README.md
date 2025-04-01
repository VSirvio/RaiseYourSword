# Raise Your Sword

*Raise Your Sword* is a 2D fantasy action game viewed from a top-down perspective. Its gameplay consists of fighting a horde of monsters emerging from off-screen.

*Made for the software development methods project course at the University of Helsinki*

## Documentation

- [Specification](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/specification.md)
- [Time tracking sheet](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/timetracking.md)
- [Changelog](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/changelog.md)

## Installation

1. Make sure you have [Python](https://www.python.org/downloads) (3.10 or newer) and [Poetry](https://python-poetry.org/docs/#installation) (1.8 or newer) installed
2. Download [the game ZIP file](https://github.com/VSirvio/RaiseYourSword/archive/refs/heads/main.zip) and extract it (or alternatively clone the repository on your computer using git)
3. On command line, go inside the game directory (The game directory is the directory that has for example the directories `documentation` and `src` inside)
3. Install the game's dependencies by running the command:

        poetry install

4. Then you can start the game by running the command:

        poetry run invoke start

## Command-line actions

### Starting the game

The game can be started using the command:

```
poetry run invoke start
```

### Testing

Tests can be run using the command:

```
poetry run invoke test
```

### Test coverage

A test coverage report can be generated using the command:

```
poetry run invoke coverage-report
```

The report will be generated to the *htmlcov* directory.

### Pylint

The checks defined in the [.pylintrc](https://github.com/VSirvio/RaiseYourSword/blob/main/.pylintrc) file can be run using the command:

```
poetry run invoke lint
```
