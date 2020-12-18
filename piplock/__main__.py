import sys
from . import main as core
from typing import Sequence


def cli(args: Sequence[str] = sys.argv):
    filepath = args[1:] and args[1]
    if not filepath:
        print('Missing <file> argument')
        exit(1)
    args = args[2:]
    if '-v' in args:
        core.VERBOSE = True
    if '-c' in args:
        core.COMPACT = True
    core.round_up(str(filepath))


if __name__ == "__main__":
    cli()