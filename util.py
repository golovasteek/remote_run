import getch
import colors

import distutils.util
import sys


def query_yes_no(question, default=None):
    if not sys.__stdin__.isatty():
        raise RuntimeError('Terminal is not interactive, cannot ask user "{}"'.format(question))

    if default == None:
        prompt = '[y/n]'
    elif distutils.util.strtobool(default):
        prompt = '[Y/n]'
    else:
        prompt = '[y/N]'

    while True:
        try:
            sys.stderr.write('{} {} '.format(question, prompt))
            sys.stderr.flush()

            answer = getch.getch()

            if answer == '\r':
                answer = default
            elif answer in '\x03\x1B': # Ctrl-C, ESC
                answer = 'no'

            print("'{}'".format(answer))

            return distutils.util.strtobool(answer)
        except ValueError:
            print(colors.colorize_error('Please answer with "y/t" or "n/f"'))

def ask_remote_failed():
    return query_yes_no(colors.colorize_error('Remote command failed. Sync results back? '), 'yes')


