from m import User, ImapAccount, db

u = User('a', 'a')
db.session.add(u)

i = ImapAccount('example.com', 'jay@example.com', 'passwd', u)
db.session.add(i)

db.session.commit()
