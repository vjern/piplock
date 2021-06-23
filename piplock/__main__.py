import sys
from . import core
from typing import List


def main(args: List[str] = sys.argv):

    args = args[1:]
    if '-v' in args:
        core.VERBOSE = True
        core.COMPACT = True
        args.pop(args.index('-v'))
    if '-c' in args:
        core.COMPACT = True
        args.pop(args.index('-c'))
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
    core.round_up(str(filepath))


if __name__ == "__main__":
    main()
