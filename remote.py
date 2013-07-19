import util

import pipes
import os
import sys

def rsync(src, dst, logFile = 'rsync.log'):
    command = 'rsync --delete --verbose --compress --archive --times -e ssh {src}/ {dst}/  >{log} 2>&1'.format(
        src = pipes.quote(src), 
        dst = pipes.quote(dst),
        log = pipes.quote(logFile))

    print(''.join([util.colorize_info('Remote syncing from '), src, util.colorize_info(' to '), dst]), end=' ', flush=True)
    result = os.system(command) == 0
    print(util.colorize_info('done') if result else util.colorize_error('failed'), flush=True)
    return result


def send(local_dir, host, remote_dir):
    remote_path = '{}:{}'.format(host, remote_dir)
    return rsync(local_dir, remote_path, 'upsync.log')


def receive(local_dir, host, remote_dir):
    remote_path = '{}:{}'.format(host, remote_dir)
    return rsync(remote_path, local_dir, 'downsync.log')


def remote_exec(host, remote_dir, command):
    full_command = 'cd {remote_dir}; {command}'.format(
        remote_dir = pipes.quote(remote_dir),
        command = ' '.join(map(pipes.quote, command)) if command else '$SHELL')
    local_command = 'ssh -t {host} {command}'.format(
        host = pipes.quote(host),
        command = pipes.quote(full_command))

    print('{} {}'.format(util.colorize_info('Executing'), local_command))
    return os.system(local_command) == 0


