import distutils.util

COLORS = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'], range(30, 38)))
def colorize(str, color = 'white', bold = False):
    enableSeq = '\x1B[{}m'.format(COLORS[color])
    if bold:
        enableSeq += '\033[1m'
    disableSeq = '\033[0m'

    return '{}{}{}'.format(enableSeq, str, disableSeq)

def colorizeInfo(str):
    return colorize(str, 'yellow', True)

def colorizeError(str):
    return colorize(str, 'red', True)

def queryYesNo(question, default=None):
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

