import sys
from . import core
from typing import List


def _help():
    return """
piplock [FILE] [OPTIONS]

FILE defaults to 'requirements.txt' if omitted.

Options:
    -c      Compact (no comments or empty lines)
    -v      Verbose (extra logs for debug purposes)
    -s      Sorted (will sort the output)
    -i      Inplace (file will be edited inplace)
    -y, -q  Set 'yes' answer as default answer to all prompts
"""


def main(args: List[str] = sys.argv):

    args = args[1:]
    if {'-h', '--help', 'help'} & set(args):
        print(_help())
        exit(0)
    if '-v' in args:
        core.VERBOSE = True
        core.COMPACT = True
        args.pop(args.index('-v'))
    if '-c' in args:
        core.COMPACT = True
        args.pop(args.index('-c'))
    if '-s' in args:
        core.SORTED = True
        args.pop(args.index('-s'))
    if '-i' in args:
        core.INPLACE = True
        args.pop(args.index('-i'))
    if '-y' in args:
        core.YESMAN = True
        args.pop(args.index('-y'))
    if '-q' in args:
        core.YESMAN = True
        args.pop(args.index('-q'))

    core.err(f'{args = }')

    if not args:
        return core.implicit()

    filepath = args[0]
    core.round_up(str(filepath), inplace=core.INPLACE)


if __name__ == "__main__":
    main()
