import configtools
import argparse
import util
import remote

import logging
import os
import sys


def _configure_logging(args):
    if 'log_level' in args:
        logging.getLogger().setLevel(args['log_level'])


class BasicAction:
    def __init__(self, args):
        self.config = args
        _configure_logging(args)

    def launch(self):
        raise RuntimeError('Can not launch basic action')


class ConfigurableAction(BasicAction):
    def __init__(self, args):
        config_from_file = configtools.get_settings()
        config_from_file.update(args)
        args = config_from_file

        super().__init__(args)


class SendAction(ConfigurableAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        return remote.send(self.config['local_root'], self.config['remote_host'], self.config['remote_root'])


class ReceiveAction(ConfigurableAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        return remote.receive(self.config['local_root'], self.config['remote_host'], self.config['remote_root'])


def _receive_if_failed(config):
    if 'receive_if_failed' not in config or config['receive_if_failed'] == 'ask':
        try:
            return util.ask_remote_failed()
        except RuntimeError as e:
            logging.warning(str(e))
            logging.warning("Assume ansver is 'no'")
            return False
    else:
        return config['receive_if_failed'] == 'yes'
        

class RemoteRunAction(ConfigurableAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        sent = remote.send(self.config['local_root'], self.config['remote_host'], self.config['remote_root'])
        
        if sent:
            result = remote.remote_exec(self.config['remote_host'], self.config['remote_dir'], self.config['command'])

            if result or _receive_if_failed(self.config):
                remote.receive(self.config['local_root'], self.config['remote_host'], self.config['remote_root'])
            else:
                logging.warning('Result not synced from server.')
                logging.info('To sync it manually use' + ' `' + sys.argv[0] + ' -r`')


class InitAction(BasicAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        configtools.create_initial_config()


class IsConfiguredAction(BasicAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        # TODO: relaise it
        try:
            configtools.get_settings()
            return True
        except:
            return False

