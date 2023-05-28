# randonautentropy

[![PyPI version](https://badge.fury.io/py/randonautentropy.svg)](https://pypi.org/project/randonautentropy/) [![PyPI - License](https://img.shields.io/pypi/l/randonautentropy)](https://pypi.org/project/randonautentropy/)

This project provides tools for interacting with The Randonautica Quantum Random Number Generator. It communicates with the JSON API and provides a Python API, and a `rndo` command-line tool.

## Installation

```
$ pip install randonautentropy
```
## Python API

The randonautentropy Python module contains a low-level `get` function.

```Python
>>> import randonautentropy as rndo

>>> rndo.get(type='hex16', length=10)

5b779d67eda68636cb90

>>> rndo.get(type='int32')

-968449906

>>> rndo.get(type='uniform')

0.9251141917698646

>>> rndo.get(type='normal')

0.8924809489412333

>>> rndo.get(type='base64')

JA==
```

## Command Line Interface

The package also comes with a `rndo` CLI:

```
usage: rndo [-h] [--hex] [--int] [--uniform] [--gauss] [--base64] [bytes]

A tool for printing random data from the Randonautica Quantum Random Number Generators

positional arguments:
  bytes                 amount of hexadecimal bytes

options:
  -h, --help            show this help message and exit
  --hex                 Hexadecimal entropy
  --int, -i             Random 32 bit integer
  --uniform, -u         Random uniform float
  --gauss, --normal, -g, -n
                        Random normal distributed float
  --base64, -b64, -b    Random uniform float
  ```

  ### Example:

  ```
  $ rndo 100
  d204ab96505929325292d84a1217ded8de5781a449be0371cdcc97e6f6b1fe69a6b530cdf7112250172e573fe7b42b9e89fe42eef198cce0ec7a427b74f59b7b7a3d8ecabfc0f0051fe06104b1dd7f2a7d1626d7f66aac5afe002bdb255ec136d52405c2

  $ rndo -u
  0.12742354174572768
  ```