import pipes
import os
import sys
import logging
import subprocess

def rsync(src, dst):
    options = ('--delete', '--verbose', '--compress', '--archive', '-e', 'ssh -q')
    command = ('rsync',) + options + (src + '/', dst + '/')

    logging.info('Remote syncing from {} to {} '.format(src, dst))
    logging.debug('Command: {}'.format(command))

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        logging.debug('rsync: ' + line.decode('utf-8').rstrip())
    for line in process.stderr:
        logging.error('rsync: ' + line.decode('utf-8').rstrip())
    result = (process.wait() == 0)

    if result:
        logging.info('Syncing done')
    else:
        logging.error('Syncing failed')
    return result


def send(local_dir, host, remote_dir):
    remote_path = '{}:{}'.format(host, remote_dir)
    return rsync(local_dir, remote_path)


def receive(local_dir, host, remote_dir):
    remote_path = '{}:{}'.format(host, remote_dir)
    return rsync(remote_path, local_dir)


def remote_exec(host, remote_dir, command):
    full_command = 'cd {remote_dir}; {command}'.format(
        remote_dir = pipes.quote(remote_dir),
        command = ' '.join(map(pipes.quote, command)) if command else '$SHELL')
    local_command = 'ssh {args} -t {host} {command}'.format(
        args = '-q' if command else '',
        host = pipes.quote(host),
        command = pipes.quote(full_command))

    logging.info('Executing {}'.format(local_command))
    return os.system(local_command) == 0

