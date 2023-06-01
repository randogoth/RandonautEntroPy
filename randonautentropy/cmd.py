import sys
import argparse
from . import rndo
from . import temporal

def main():

    parser = argparse.ArgumentParser(description="A tool for printing random data from the Randonautica Quantum Random Number Generators")
    parser.add_argument("--rndo", "-r", action="store_false", help="Hexadecimal QRNG entropy")
    parser.add_argument("--temporal", "-t", action="store_true", help="Hexadecimal Temporal entropy")
    parser.add_argument("bytes", nargs="?", type=int, default=10, help="amount of hexadecimal bytes")
    parser.print_usage = parser.print_help
    args = parser.parse_args()

    generator = None

    if args.temporal:
        try:
            bytes = int(args.bytes)
        except ValueError:
            sys.exit(1)
        generator = temporal.get(bytes)
    elif args.rndo:
        try:
            bytes = int(args.bytes)
        except ValueError:
            sys.exit(1)
        generator = rndo.get(bytes)

    if not generator:
        sys.exit(1)
    try:
        print(generator)
    except:
        pass

if __name__ == '__main__':
    main()
