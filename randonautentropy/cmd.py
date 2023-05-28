# Copyright 2023 randogoth <tobias@randonauts.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
A tool for printing random data from the Randonautica Quantum Random Number Generators
"""
from __future__ import print_function

import sys
from . import rndo
import argparse

def main():

    parser = argparse.ArgumentParser(description="A tool for printing random data from the Randonautica Quantum Random Number Generators")
    parser.add_argument("--hex", action="store_false", help="Hexadecimal entropy")
    parser.add_argument("--int", "-i", action="store_true", help="Random 32 bit integer")
    parser.add_argument("--uniform", "-u", action="store_true", help="Random uniform float")
    parser.add_argument("--gauss", "--normal", "-g", "-n", action="store_true", help="Random normal distributed float")
    parser.add_argument("--base64", "-b64", "-b", action="store_true", help="Random uniform float")
    parser.add_argument("bytes", nargs="?", type=int, default=10, help="amount of hexadecimal bytes")
    parser.print_usage = parser.print_help
    args = parser.parse_args()

    generator = None

    if args.hex:
        try:
            bytes = int(args.bytes)
        except ValueError:
            sys.exit(1)
        generator = rndo.get('hex16', bytes)

    if args.int:
        print(rndo.get('int32'))
        sys.exit(0)

    if args.uniform:
        print(rndo.get('uniform'))
        sys.exit(0)

    if args.gauss:
        print(rndo.get('normal'))
        sys.exit(0)

    if args.base64:
        print(rndo.get('base64'))
        sys.exit(0)

    if not generator:
        sys.exit(1)
    try:
        print(generator)
    except:
        pass

if __name__ == '__main__':
    main()
