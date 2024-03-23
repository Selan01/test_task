# Project Configuration Stuff
## Enforcing Configuration

Enforcing is done with the help of nitpick — a command-line tool.

### Installation

Install nitpick:

```sh
pipx install nitpick
```

### Usage

To check for errors only:

```sh
nitpick check
```

To fix and modify your files directly:
```sh
nitpick fix
```

## Initializing a Project
### Python

```sh
cookiecutter https://gitea.radium.group/radium/project-configuration.git --directory cookiecutter-python
```
