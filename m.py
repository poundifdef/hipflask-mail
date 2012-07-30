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
    return User.query.filter_by(id=id).first()

login_manager.setup_app(app)
login_manager.login_view = "loginpage"

class User(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    salt = db.Column(db.String(32), unique=False, nullable=False)
    passwd = db.Column(db.String(60), unique=False, nullable=False)

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
    # TODO: add name field
    server = db.Column(db.String(128), unique=False)
    email = db.Column(db.String(128), unique=False, nullable=False)
    passwd = db.Column(db.String(128), unique=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
        backref=db.backref('imapaccounts', lazy='dynamic'))

    def __init__(self, server, email, password, user):
        self.server = server
        self.email = email
        self.passwd = password
        self.user = user

    def __repr__(self):
        return '<Imap Account %r>' % (self.email)


@app.route('/', methods=['GET', 'POST'])
def loginpage():
    def check_credential(u):
        return u and hashpw(password, u.salt) == u.passwd

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        u = User.query.filter_by(email=username).first()

        if check_credential(u):
            login_user(u)
        else:
            flash('bad command or file name')

    if current_user.is_anonymous():
        return render_template('login.html')

    return redirect(url_for("mail"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("loginpage"))

@app.route('/admin/mail/delete', methods=['POST'])
@login_required
def admin_delete():
    try:
        a = ImapAccount.query.filter_by(
            id=request.form.get('delete_id')
            ).first()

        db.session.delete(a)
        db.session.commit()
    except Exception as ex:
        flash('could not delete: ' + str(ex))

    return redirect(url_for("admin_mail"))

@app.route('/admin/mail', methods=['GET', 'POST'])
@login_required
def admin_mail():
    def verify_imap_credential(server, email, passwd):
        import imaplib
        try:
            m = imaplib.IMAP4_SSL(request.form.get('server', ''))
            m.login(email, passwd)
            m.logout()
            return True
        except Exception as ex:
            flash("didn't work: " + str(ex))
            pass

    if request.method == 'POST':
        server = request.form.get('server')
        email = request.form.get('email')
        passwd = request.form.get('passwd')

        if verify_imap_credential(server, email, passwd):
            i = ImapAccount(server, email, passwd, current_user)
            db.session.add(i)
            db.session.commit()
            flash('horray! it worked!')

    page_info = {}
    page_info['mailboxes'] = ImapAccount.query.filter_by(user_id=current_user.id).all()
    return render_template('admin_email.html', **page_info)

@app.route("/mail")
@login_required
def mail():
    page_info = {}
    page_info['mailboxes'] = ImapAccount.query.filter_by(user_id=current_user.id).all()
    return render_template('email.html', **page_info)


if __name__ == "__main__":
    db.create_all()

    # app.run()
    app.run(host='0.0.0.0', debug=True)

