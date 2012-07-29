from flask import Flask, request, render_template, redirect, url_for, flash

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

from bcrypt import gensalt, hashpw
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    #return None
    return User('a','b')

login_manager.setup_app(app)

class User(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    salt = db.Column(db.String(32), unique=False)
    passwd = db.Column(db.String(60), unique=False)

    emails = db.relationship

    def __init__(self, email, password):
        self.email = email

        salt = gensalt(10)
        self.salt = salt
        self.passwd = hashpw(password, salt)

    def __repr__(self):
        return '<User %r>' % (self.email)


class ImapAccount(db.Model):
    #__tablename__ = 'imap_accounts'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=False)
    passwd = db.Column(db.String(128), unique=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('imapaccounts', lazy='dynamic'))

    def __init__(self, name, email, password, user):
        self.name = name
        self.email = email
        self.passwd = password
        self.user = user

    def __repr__(self):
        return '<Imap Account %r>' % (self.email)

#from models import User, ImapAccount

#@app.teardown_request
#def shutdown_session(exception=None):
#    db_session.remove()

@app.route("/")
def loginpage():
    if True:
       login_user(User('a','b'))
       return redirect(url_for("hello"))
    else:
        logout_user()

    return 'nope'


@app.route("/mail")
@login_required
def hello():
    users = User.query.all()
    return str(current_user.__dict__)
    return '<pre>' + str([u.email for u in users]) + '</pre>'

if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', debug=True)

