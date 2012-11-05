import os

# Path to contain all hipflask data: maildirs, user accounts, sqlite DBs, etc
HIPFLASK_DATA = './data'
HIPFLASK_FOLDERS = {
    'sqlite': os.path.abspath(HIPFLASK_DATA + '/sqlite'),
    'mu': os.path.abspath(HIPFLASK_DATA + '/mu'),
    'offlineimap': os.path.abspath(HIPFLASK_DATA + '/offlineimap'),
    'maildirs': os.path.abspath(HIPFLASK_DATA + '/maildirs'),
}

HIPFLASK_SQLITE_NAME = 'hipflask-mail.db'
HIPFLASK_SQLITE_CONN = 'sqlite:///%s/%s' % (HIPFLASK_FOLDERS['sqlite'],
                                            HIPFLASK_SQLITE_NAME)

HIPFLASK_OFFLINEIMAPRC = 'offlineimaprc'

for key, folder in HIPFLASK_FOLDERS.iteritems():
    if not os.path.exists(folder):
        os.makedirs(folder)
