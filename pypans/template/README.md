![Screenshot](icon.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/vyahello/<package>.svg?branch=master)](https://travis-ci.org/vyahello/<package>)
[![Coverage Status](https://coveralls.io/repos/github/vyahello/<package>/badge.svg?branch=master)](https://coveralls.io/github/vyahello/<package>?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with pylint](https://img.shields.io/badge/pylint-checked-blue)](https://www.pylint.org)
[![Checked with flake8](https://img.shields.io/badge/flake8-checked-blue)](http://flake8.pycqa.org/)
[![Checked with pydocstyle](https://img.shields.io/badge/pydocstyle-checked-yellowgreen)](http://www.pydocstyle.org/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)

# <package>

> A brief description for **<package>** tool.

## Tools

- python 3.6 | 3.7 | 3.8
- [travis](https://travis-ci.org/) CI
- code analysis
  - [pytest](https://pypi.org/project/pytest/)
  - [black](https://black.readthedocs.io/en/stable/)
  - [mypy](http://mypy.readthedocs.io/en/latest)
  - [pylint](https://www.pylint.org/)
  - [flake8](http://flake8.pycqa.org/en/latest/)
  - [pydocstyle](https://github.com/PyCQA/pydocstyle)

## Usage

![Usage](usage.gif)

### Quick start

```bash
pip install <package>
✨ 🍰 ✨
```

After please run **<package>** tool from your shell:
```bash
<package>
```

### Source code

```bash
git clone path/to/github/repo.git
pip install -e .
<package>
```

Or using direct release:
```bash
pip install git+https://path/to/github/repo@0.0.1
<package>
```

### Local debug

```bash
git clone path/to/github/repo.git
python -m <package>
```
**[⬆ back to top](#<package>)**

## Development notes

### Testing

Generally, `pytest` tool is used to organize testing procedure.

Please follow next command to run unittests:
```bash
pytest
```

### CI

Project has Travis CI integration using [.travis.yml](.travis.yml) file thus code analysis (`black`, `pylint`, `flake8`, `mypy`, `pydocstyle`) and unittests (`pytest`) will be run automatically after every made change to the repository.

To be able to run code analysis, please execute command below:
```bash
./analyse-source-code.sh
```
### Release notes

Please check [changelog](CHANGELOG.md) file to get more details about actual versions and it's release notes.

### Meta

Author – _<username>_. Please check [authors](AUTHORS.md) file for more details.

Distributed under the `MIT` license. See [license](LICENSE.md) for more information.

You can reach out me at:
* [<email>](<email>)
* [https://github.com/<username>](https://github.com/<username>)
* [https://www.linkedin.com/in/<username>](https://www.linkedin.com/in/<username>)

### Contributing
1. clone the repository
2. configure Git for the first time after cloning with your `name` and `email`
3. `pip install -r requirements.txt` to install all project dependencies
4. `pip install -r requirements-dev.txt` to install all development project dependencies

**[⬆ back to top](#<package>)**