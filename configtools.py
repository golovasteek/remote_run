import os
import os.path
import configparser
import distutils.util
import textwrap

CONFIG_FILE_NAME = ".remoterun"

def findConfig(directory):
    while True:
        configFile = os.path.join(directory, CONFIG_FILE_NAME)
        if os.path.exists(configFile):
            return configFile

        directory, splitted = os.path.split(directory)
        if not splitted:
            raise RuntimeError("RemoteRun not configured for this directory");

def parseConfig(configFile):
    configParser = configparser.ConfigParser()
    configParser.read(configFile)

    receiveIfFailed = configParser.get('main', 'receiveIfFailed', fallback='ask')

    return {
        'remoteHost' : configParser.get('main', 'remoteHost'),
        'remoteRoot' : configParser.get('main', 'remoteDir'),
        'receiveIfFailed' : distutils.util.strtobool(receiveIfFailed) if receiveIfFailed != 'ask' else None
        }

def getSettings():
    localDir = os.path.realpath(os.curdir)
    configFile = findConfig(localDir)
    localRoot = os.path.dirname(configFile)

    settings = {
        'localDir' : localDir,
        'localRoot' : localRoot,
        'relPath' : os.path.relpath(localDir, localRoot)
        }

    settings.update(parseConfig(configFile))
    settings['remoteDir'] = os.path.normpath(os.path.join(settings['remoteRoot'], settings['relPath']))

    return settings

def createInitialConfig():
    defaultConfigTextRaw = '''
        ##############################################
        # This is a initial remote run config
        # Set next options:

        [main]
        
        # Url of host to sync
        # Example: remoteHost = yandex.ru
        remoteHost =  

        # Path on the remote host to sync with
        # Example: remoteDir = /home/foo/rr/
        remoteDir =  

        #############################################
        # You can also select some optional arguments

        # Receive or not if remote command failed (yea/no/ask)
        # receiveIfFailed = ask
    '''
    defaultConfigText = textwrap.dedent(defaultConfigTextRaw).strip()

    if os.path.exists(CONFIG_FILE_NAME):
        raise RuntimeError('Config is already saved in {}'.format(CONFIG_FILE_NAME)) 

    with open(CONFIG_FILE_NAME, mode='w') as configFile:
        print(defaultConfigText, file=configFile)

    os.system('vim {} +9'.format(CONFIG_FILE_NAME))


