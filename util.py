import distutils.util

COLORS = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'], range(30, 38)))


def colorize(str, color = 'white', bold = False):
    enable_seq = '\x1B[{}m'.format(COLORS[color])
    if bold:
        enable_seq += '\033[1m'
    disable_seq = '\033[0m'

    return '{}{}{}'.format(enable_seq, str, disable_seq)


def colorize_info(str):
    return colorize(str, 'yellow', True)


def colorize_error(str):
    return colorize(str, 'red', True)


def query_yes_no(question, default=None):
    if default == None:
        prompt = '[y/n]'
    elif distutils.util.strtobool(default):
        prompt = '[Y/n]'
    else:
        prompt = '[y/N]'

    while True:
        try:
            answer = input('{} {} '.format(question, prompt))
            if answer == '':
                answer = default
            return distutils.util.strtobool(answer)
        except:
            print('Please answer with "yes" or "no".')

def ask_remote_failed():
    return query_yes_no(colorize_error('Remote command failed. Sync results back? '), 'yes')


