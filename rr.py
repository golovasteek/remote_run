#! /usr/bin/env python3

import actions
import util

import sys
import argparse


def createArgParser():
    parser = argparse.ArgumentParser(
        description='''
            Sync file tree to the remote host, run specified command, and sync result back.
            ''',
        usage='\n\t{}\n\t{}\n\t{}'.format(
            '%(prog)s [options] [command [arg ... ]]',
            '%(prog)s [options] [-r | -s]',
            '%(prog)s -h'),
        add_help=False)

    actions = parser.add_argument_group('Actions')
    actions.add_argument('command', nargs=argparse.REMAINDER, default = [],
        help='command to run remote (runs shell by default)')
    otherActions = actions.add_mutually_exclusive_group()
    otherActions.add_argument('--init', action='store_true',
        help='initialize rr in current directory')
    otherActions.add_argument('-r', '--receive-only', action='store_true',
        dest='receiveOnly',
        help='only sync data from remote host')
    otherActions.add_argument('-s', '--send-only', action='store_true',
        dest='sendOnly',
        help='only sync data to remote host')

    options = parser.add_argument_group('Options')
    forceOptions = options.add_mutually_exclusive_group()
    forceOptions.add_argument('-f', '--receive-if-failed', action='store_true',
        dest='receiveIfFailed',
        help='if remote command failed receive data without asking')
    forceOptions.add_argument('-n', '--not-receive-if-failed', action='store_true',
        dest='notReceiveIfFailed',
        help='if remote command failed do not receive data')

    others = parser.add_argument_group('Other arguments')
    others.add_argument('-h', '--help', action='help', help='show this help message and exit')
    others.add_argument('-c', '--is-configured', action='store_true',
        dest='isConfigured',
        help='test if current dir is configured for rr')

    return parser

def parseArgs(argv):
    result = dict(vars(createArgParser().parse_args(argv[1:])))

    if len(result['command']) != 0 and (result['receiveOnly'] or result['sendOnly']):
        raise ArgumentError('Command can not be specified if --receive-only or --send-only flags enabled')

    if not (result['receiveIfFailed'] or result['notReceiveIfFailed']):
        del result['receiveIfFailed'] 
    del result['notReceiveIfFailed']

    return result

def main(argv):
    try:
        args = parseArgs(argv)        
        action = actions.createAction(args)
    except Exception as exc:
        print(util.colorizeError(exc))
        return 1

    try:
        actionSucceed = action.launch()
        return 0 if actionSucceed else -1
    except Exception as exc:
        print(util.colorizeError(exc))
        return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv))
