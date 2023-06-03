# RandonautEntroPy

[![PyPI version](https://badge.fury.io/py/randonautentropy.svg)](https://pypi.org/project/randonautentropy/) [![PyPI - License](https://img.shields.io/pypi/l/randonautentropy)](https://pypi.org/project/randonautentropy/)

This project provides tools for interacting with the Randonautica QRNG and [Temporal](https://github.com/TheRandonauts/temporal) entropy generators. It provides a Python API, and a `rndo` command-line tool.

### Fair Use Policy

Please request only the entropy amount you really need for your project. Please note that in case of overuse the API is subject to immediate modifications and amendments to free availability.

Temporal on the other hand runs on your system and is always available.

## Installation

```
$ pip install randonautentropy
```

### Installing Temporal

The first time the `temporal.get` Python method or `rndo -t` command line option are called, a script attempts to automatically install the [TemporalLib](https://github.com/TheRandonauts/temporal) shell tool dependency in `/usr/local/bin`

In case that fails you can install it yourself:

```
$ sudo apt install git build-essential
$ git clone --depth 1 git@github.com:TheRandonauts/temporal.git
$ cd temporal
$ ./make.sh
```

---

## Python API

The randonautentropy Python module contains low-level `get` functions.

```Python
>>> from randonautentropy import rndo
>>> from randonautentropy import temporal

>>> rndo.get(length=10, type='hex16')

e5b779d67eda68636cb9

>>> temporal.get(length=10, channel=0)

d0c7ca53cb57ede1be14
```

### Extended Functionality

The `rndo.get` function can also retrieve a single 32bit random number in different formats:
```Python
>>> rndo.get(type='int32')

-968449906

>>> rndo.get(type='uniform')

0.9251141917698646

>>> rndo.get(type='normal')

0.8924809489412333

>>> rndo.get(type='base64')

JA==
```
The `temporal.get` method can switch from the default high quality entropy mode to a faster but slightly lower entropy mode by switching its `channel` to 1.

```Python
>>> temporal.get(channel=1)

b83a7fd79bee5b3b1ad7

```

---

## Command Line Interface

The package also comes with a `rndo` CLI:

```
usage: rndo [-h] [--rndo] [--temporal] [bytes]

A tool for printing random data from the Randonautica Quantum Random Number Generators

positional arguments:
  bytes           amount of hexadecimal bytes

options:
  -h, --help      show this help message and exit
  --rndo, -r      Hexadecimal QRNG entropy
  --temporal, -t  Hexadecimal Temporal entropy
  ```

  ### Example:

  ```
  $ rndo -r 100
  d204ab96505929325292d84a1217ded8de5781a449be0371cdcc97e6f6b1fe69a6b530cdf7112250172e573fe7b42b9e89fe42eef198cce0ec7a427b74f59b7b7a3d8ecabfc0f0051fe06104b1dd7f2a7d1626d7f66aac5afe002bdb255ec136d52405c2

  $ rndo -t 100
  93378573b635dc2b01ffd426068e6ccecbc2046fbc9598c1c41a4cbe0dcc8f62071202ea72d05b83581e8cd968cbd099ee0ccf37e9fbcd7d476bd4da6b1965434fc1a65302c732a06b6e5cebff37101a21926a34f1b236a4660a599c6ec93ae7296176fc
  ```