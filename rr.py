#! /usr/bin/env python3

import arg_parser
import util

import sys

def parse_args(argv):
    parser = arg_parser.RemoteRunArgParser()
    return parser.parse(argv[1:])


def main(argv):
    try:
        args = parse_args(argv)
        action = args['action'](args)
        action.launch()

    except Exception as exc:
        print(util.colorize_error(str(exc)))
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
