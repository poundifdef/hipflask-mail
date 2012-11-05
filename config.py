import os

# Path to contain all hipflask data: maildirs, user accounts, sqlite DBs, etc
HIPFLASK_DATA = './data'
HIPFLASK_FOLDERS = {
    'sqlite': 'sqlite',
    'mu': 'mu',
    'offlineimap': 'offlineimap',
    'maildirs': 'maildirs'
}

HIPFLASK_SQLITE_NAME = 'hipflask-mail.db'
HIPFLASK_SQLITE_CONN = 'sqlite:///%s/%s/%s' % (HIPFLASK_DATA, 
                                               HIPFLASK_FOLDERS['sqlite'],
                                               HIPFLASK_SQLITE_NAME)

for key, folder in HIPFLASK_FOLDERS.iteritems():
    if not os.path.exists('%s/%s' % (HIPFLASK_DATA, folder)):
        os.makedirs('%s/%s' % (HIPFLASK_DATA, folder))
