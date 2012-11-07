from subprocess import call, Popen, PIPE
from pprint import pprint

import base64
import config
import urllib

class MaildirUtils:
    def __init__(self, account):
        self.account = account

    def get_message(self, msg_path):
        cmd = [
            'mu',
            'view',
            msg_path,
            '--muhome=%s' % config.HIPFLASK_FOLDERS['mu']
        ]

        p = Popen(cmd, stdout=PIPE).stdout
        message = p.read()
        p.close()

        # TODO: make this a dict of fields
        return message

    def _get_fields(self, msg_path, length=50):
        cmd = [
            'mu',
            'view',
            msg_path,
            '--summary-len=5',
            '--muhome=%s' % config.HIPFLASK_FOLDERS['mu']
        ]

        p = Popen(cmd, stdout=PIPE).stdout
        fields = p.read().splitlines()
        p.close()

        message = {}
        for field in fields:
            separator = field.find(':')
            
            if separator == -1:
                continue

            key = field[0:separator].lower()
            value = field[separator+2:]
            if len(value) > length:
                value = value[:length] + '...'
            message[key] = value

        return message


    def get_messages(self, email, folder, start, length):
        p = Popen([
            'mu',
            'find',
            '--muhome=%s' % config.HIPFLASK_FOLDERS['mu'],
            'maildir:/%s/%s' % (email, folder),
            '--sortfield=date',
            '--reverse',
            '--format=plain',
            '--fields',
            'g l'
            #'g l'
        ], stdout=PIPE).stdout
        # TODO: search/filter?
        all_lines = p.read().splitlines()
        lines = all_lines[start:start+length]

        p.close()

        messages = []
        for l in lines:
            msg_path = l
            #print len(l.split(' '))
            #flags, msg_path = set(l.split(' '))
            s = l.split(' ')
            flags = s[0]
            msg_path = s[1]
            #flags, msg_path = set(l.split(' '))
            #print msg_path
            message = self._get_fields(msg_path)
            message['seen'] = 'S' in flags
            message['path'] = urllib.quote(base64.b64encode(msg_path))
                
            messages.append(message)

        return len(all_lines), messages


if __name__ == '__main__':
    m = MaildirUtils('account')
    print m.get_messages('folder', 0, 6)
