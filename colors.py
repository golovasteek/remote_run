import ctypes
import logging


def _escape_sequences():
    csi = '\x1b['
    reset = '\x1b[0m'
    colors = tuple(enumerate(('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')))

    result = dict(('esc-{}'.format(name), '\x1B[{}m'.format(number + 30)) for number, name in colors)
    result.update(('esc-bg-{}'.format(name), '\x1B[{}m'.format(number + 40)) for number, name in colors)
    result.update({'esc-bold' : '\033[1m'})
    result.update({'esc-reset' : '\033[0m'})

    return result


def _level_escape_sequences():
    escape_sequences = _escape_sequences()
    return dict((key, code.format_map(escape_sequences)) for key, code in (
        ('esc-debug', '{esc-blue}'),
        ('esc-info', '{esc-green}'),
        ('esc-warning', '{esc-yellow}'),
        ('esc-error', '{esc-red}{esc-bold}'),
        ('esc-critical', '{esc-white}{esc-bg-red}{esc-bold}')))


ESCAPE_SEQUENCES = _escape_sequences()
ESCAPE_SEQUENCES.update(_level_escape_sequences())


def format_colorized(s):
    return s.format_map(ESCAPE_SEQUENCES)


def print_colorized(*args, **kwargs):
    print(*map(format_colorized, args), **kwargs)


def colorize_info(s):
    return format_colorized('{esc-info}' + s + '{esc-reset}')


def colorize_error(s):
    return format_colorized('{esc-error}' + s + '{esc-reset}')


class ColorizingStreamHandler(logging.StreamHandler):
    """ Colorized logging handleer

    Inspired by http://plumberjack.blogspot.ru/2010/12/colorizing-logging-output-in-terminals.html
    Currenty there is no Windows support. To add it you can follow instructions in that topic.
    """

    def _is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def emit(self, record):
        try:
            self.stream.write(self.format(record))
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def format(self, record):
        message = super().format(record)
        if self._is_tty():
            # Don't colorize any traceback
            parts = message.split('\n', 1)
            parts[0] = self._colorize(parts[0], record.levelno)
            message = '\n'.join(parts)
        return message

    _level_colors = {
        logging.DEBUG: '{esc-debug}',
        logging.INFO: '{esc-info}',
        logging.WARNING: '{esc-warning}',
        logging.ERROR: '{esc-error}',
        logging.CRITICAL: '{esc-critical}',
    }
    _colors_off = '{esc-reset}'

    def _colorize(self, message, level):
        if level in self._level_colors:
            return format_colorized(self._level_colors[level] + message + self._colors_off)
        else:
            return message

