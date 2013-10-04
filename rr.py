#! /usr/bin/env python3

import arg_parser
import colors

import logging
import sys

def parse_args(argv):
    parser = arg_parser.RemoteRunArgParser()
    return parser.parse(argv[1:])


def main(argv):
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level='INFO',
        handlers=[colors.ColorizingStreamHandler(sys.stderr)])

    try:
        args = parse_args(argv)
        action = args['action'](args)
    except Exception as exc:
        logging.exception(exc)
        return 1
        
    try:
        return not action.launch()
    except Exception as exc:
        if 'log_level' in action.config and action.config['log_level'] == 'DEBUG':
            logging.exception(exc)
        else:
            logging.error(str(exc))
        return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv))
