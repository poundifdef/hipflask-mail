from subprocess import call, Popen, PIPE
from pprint import pprint

import config

class MaildirUtils:
    def __init__(self, account):
        self.account = account

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
            'l'
        ], stdout=PIPE).stdout
        # TODO: search/filter?
        all_lines = p.read().splitlines()
        lines = all_lines[start:start+length]

        p.close()

        messages = []
        for l in lines:
            message = self._get_fields(l)
            messages.append(message)

        return len(all_lines), messages


if __name__ == '__main__':
    m = MaildirUtils('account')
    print m.get_messages('folder', 0, 6)
