# YTMusicDL

![Supported Python versions](https://img.shields.io/pypi/pyversions/noveldown)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Download from PyPI](https://img.shields.io/pypi/v/ytmusicdl)](https://pypi.org/project/ytmusicdl)
[![Latest release](https://img.shields.io/github/v/release/potatoeggy/ytmusicdl?display_name=tag)](https://github.com/potatoeggy/ytmusicdl/releases/latest)
[![License](https://img.shields.io/github/license/potatoeggy/ytmusicdl)](/LICENSE)

Webnovel downloader and converter to EPUB (with metadata!) as a Python library and command line application.

## Installation

Install the package from PyPI:

```
pip3 install ytmusicdl
```

Or, to build from source:

YTMusicDL depends on [poetry](https://github.com/python-poetry/poetry) for building.

```
git clone https://github.com/potatoeggy/ytmusicdl.git
poetry install
poetry build
pip3 install dist/ytmusicdl*.whl
```
