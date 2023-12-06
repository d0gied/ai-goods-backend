# Global module for all project

## Overview

This module contains global definitions and functions that are used in other modules and services.

## Installation

In service folder open `pyproject.toml` and add the following lines:

```toml
[tool.poetry.dependencies]
global_modules = {path = "../global_modules"}
```

Then run `poetry lock` to update `poetry.lock` file. And then run `poetry install` to install the module.

## Usage

To use the module in your code, add the following line:

```python
from global_modules import <name>
```

## Development

To develop the module, you need to install `poetry`:

```bash
pip install poetry
```

Then you can install the module in editable mode:

```bash
poetry install
```

Do development and run tests.

```bash
poetry run pytest
```

## Deployment

To update dependencies in all services, run the following script:

### Linux/MacOS

```bash
. ./rebuild_global_modules.sh
```

### Windows

```powershell
./rebuild_global_modules.ps1
```

## License

This project is licensed under the terms of the MIT license.