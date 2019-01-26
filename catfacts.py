from flask import Flask, render_template, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from os import path, environ
import random
import json

script_dir = path.dirname(__file__)

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key      = environ.get("CATFACTS_KEY", "K2ptdnpfjLnFrA2c")
catfact_user        = environ.get("CATFACTS_USER", "catdaddy")
catfact_pass        = environ.get("CATFACTS_PASS", "fxVVC8GQNTvUbeJn")
secret_bonus_fact   = environ.get("CATFACTS_BONUS_FACT")
cert_path           = environ.get("CERT_PATH", path.join(script_dir, "certs/localhost.cert"))
key_path            = environ.get("KEY_PATH", path.join(script_dir, "certs/localhost.key"))

class LonelyUser(UserMixin):
    id = catfact_pass

lonely_user = LonelyUser()

class LoginForm(FlaskForm):
    user = TextField('Username', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    if user_id == lonely_user.get_id():
        return lonely_user
    else:
        return None

class CatFacts:
    def __init__(self, factfile=None, exclfile=None):
        self.facts = []
        self.exclamations = []

        self.load(factfile, exclfile)

    def load(self, factfile, exclfile):
        if factfile:
            with open(factfile) as f:
                self.facts = list(enumerate(json.load(f)))

        if exclfile:
            with open(exclfile) as f:
                self.exclamations = list(json.load(f))

    def random(self):
        num, fact = random.choice(self.facts)
        exclamation = random.choice(self.exclamations)
        return num, fact, exclamation

thefacts = CatFacts()

@app.route('/login', methods=('POST',))
def login():
    form = LoginForm()
    sucess = False
    if form.validate_on_submit():
        if form.user.data == catfact_user and form.passwd.data == catfact_pass:
            login_user(lonely_user)
            sucess = True
        else:
            flash('Credentials rejected: You are not a true Cat Daddy')
    else:
        flash('Please enter your credentials')

    if sucess:
        return redirect("#")
    else:
        return redirect("#login")

@app.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    return redirect('#')


@app.route('/')
def hello_world():
    num, fact, exclamation = thefacts.random()
    form = LoginForm()
    return render_template(
            'fact.html', 
            fact=fact,
            num=num,
            exclamation=exclamation,
            secret_bonus_fact=secret_bonus_fact,
            login_form=LoginForm()
            )

if __name__ == '__main__':
    factfile = path.join(script_dir, 'catfacts.json')
    exclfile = path.join(script_dir, 'exclamations.json')
    thefacts.load(factfile, exclfile)

    app.run(debug=True, host='0.0.0.0', port=8080, ssl_context=(cert_path, key_path))
