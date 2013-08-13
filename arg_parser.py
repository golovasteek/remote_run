import argparse
import actions
import util

DEFAULTS = dict()

def _format_usage(actions):
    return '''
    %(prog)s [options] [<command> [<arg> ... ]]
    %(prog)s [options] <action>
    %(prog)s [options] -h
    '''


def _register_actions(parser):
    action_args = parser.add_argument_group('Actions')
    exclusive_action_args = action_args.add_mutually_exclusive_group()

    action_args.add_argument(
        'command',
        nargs=argparse.REMAINDER,
        default=[],
        metavar='COMMAND',
        help='command to run remote (runs shell by default)')

    exclusive_action_args.add_argument(
        '-s',
        '--send-only',
        action='store_const',
        dest='action',
        const=actions.SendAction,
        help='only sync data to remote host')

    exclusive_action_args.add_argument(
        '-r',
        '--receive-only',
        action='store_const',
        dest='action',
        const=actions.ReceiveAction,
        help='only receive data from remote host')

    exclusive_action_args.add_argument(
        '--init',
        action='store_const',
        dest='action',
        const=actions.InitAction,
        help='initialize rr in current directory')

    exclusive_action_args.add_argument(
        '--is-configured',
        action='store_const',
        dest='action',
        const=actions.IsConfiguredAction,
        help='test if current directory is configured for rr')


def _register_other_args(parser):
    other_args = parser.add_argument_group('Other arguments')

    other_args.add_argument(
        '-e',
        '--enforce-host',
        dest='remote_host',
        help='enforce to use specified host for remote running')

    force_options = other_args.add_mutually_exclusive_group()
    force_options.add_argument(
        '-f',
        '--receive-if-failed',
        action='store_const',
        dest='receive_if_failed',
        const='yes',
        help='if remote command failed receive data without asking')
    force_options.add_argument(
        '-n',
        '--not-receive-if-failed',
        action='store_const',
        dest='receive_if_failed',
        const='no',
        help='if remote command failed do not receive data')

    other_args.add_argument(
        '-h',
        '--help',
        action='help',
        help='show this help message and exit')


class RemoteRunArgParser:
    def __init__(self):
        self._basic_parser = argparse.ArgumentParser(
            description='Sync file tree to the remote host, run specified command, and sync result back.',
            usage=_format_usage(actions),
            add_help=False)
        
        _register_actions(self._basic_parser)
        _register_other_args(self._basic_parser)

    def parse(self, args):
        args = dict((k, v) 
            for k, v in vars(self._basic_parser.parse_args(args)).items()
                if v)

        if 'action' not in args:
            args['action'] = actions.RemoteRunAction
        elif 'command' in args:
            raise argparse.ArgumentError('Command can not be specified with other action.')

        return args
