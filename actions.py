import configtools
import util

import shlex
import os
import sys

def rsync(src, dst, logFile = 'rsync.log'):
    command = 'rsync --delete --verbose --compress --archive --times -e ssh {src}/ {dst}/  >{log} 2>&1'.format(
        src = shlex.quote(src), 
        dst = shlex.quote(dst),
        log = shlex.quote(logFile))

    print(''.join([util.colorizeInfo('Remote syncing from '), src, util.colorizeInfo(' to '), dst]), end=' ', flush=True)
    result = os.system(command) == 0
    print(util.colorizeInfo('done') if result else util.colorizeError('failed'), flush=True)
    return result

def rsyncSend(localDir, host, remoteDir):
    remotePath = '{}:{}'.format(host, remoteDir)
    return rsync(localDir, remotePath, 'upsync.log')

def rsyncReceive(localDir, host, remoteDir):
    remotePath = '{}:{}'.format(host, remoteDir)
    return rsync(remotePath, localDir, 'downsync.log')

def remoteExec(host, remoteDir, command):
    fullCommand = 'cd {remoteDir}; {command}'.format(
        remoteDir = shlex.quote(remoteDir),
        command = ' '.join(map(shlex.quote, command)) if command else '$SHELL')
    localCommand = 'ssh -t {host} {command}'.format(
        host = shlex.quote(host),
        command = shlex.quote(fullCommand))

    print('{} {}'.format(util.colorizeInfo('Executing'), localCommand))
    return os.system(localCommand) == 0

class BasicAction:
    def __init__(self, args):
        self.config = args

    def launch(self):
        raise RuntimeError('Can not launch basic action')

class ConfigurableAction(BasicAction):
    def __init__(self, args):
        super().__init__(args)
        configFromFile = configtools.getSettings()
        configFromFile.update(self.config)
        self.config = configFromFile

class SendAction(ConfigurableAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        return rsyncSend(self.config['localRoot'], self.config['remoteHost'], self.config['remoteRoot'])

class ReceiveAction(ConfigurableAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        return rsyncReceive(self.config['localRoot'], self.config['remoteHost'], self.config['remoteRoot'])

def _askRemoteFailed():
    return util.queryYesNo(util.colorizeError('Remote command failed. Sync results back? '), 'yes')

class RemoteRunAction(ConfigurableAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        sent = rsyncSend(self.config['localRoot'], self.config['remoteHost'], self.config['remoteRoot'])
        
        if sent:
            result = remoteExec(self.config['remoteHost'], self.config['remoteDir'], self.config['command'])

            if (result or self.config['receiveIfFailed'] or 
                    (self.config['receiveIfFailed'] == None and _askRemoteFailed())):
                rsyncReceive(self.config['localRoot'], self.config['remoteHost'], self.config['remoteRoot'])
            else:
                print(util.colorizeInfo('Result not synced from server. To do it manually use') + ' `' + sys.argv[0] + ' -r`')

class InitAction(BasicAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        configtools.createInitialConfig()

class IsConfiguredAction(BasicAction):
    def __init__(self, args):
        super().__init__(args)

    def launch(self):
        # TODO: relaise it
        try:
            findConfig()
            return True
        except:
            return False

def createAction(args):
    optionToAction = {
        'init' : InitAction,
        'sendOnly' : SendAction,
        'receiveOnly' : ReceiveAction,
        'command' : RemoteRunAction,
        'is_configured' : IsConfiguredAction
    }

    for option, action in optionToAction.items():
        if option in args and args[option]:
            return action(args)

    return RemoteRunAction(args)
        
