from flask import Flask, render_template, redirect, request, session, url_for
from models import User
from routes.auth import auth
from routes.admin import admin
from routes.users import users
from routes.basket import basket
from routes.items import items

app = Flask(__name__)
app.debug = True

# Random os.urandom(16) secret key
app.secret_key = b'\x9a\xac\xea\x9e\xe9\xbbN\x1d\xa5\xb4\x1f\x17\xd3\xdd\x96O'

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(basket)
app.register_blueprint(items)


@app.route('/')
def index():
    return redirect('/auth')


@app.route('/home')
def home():
    return redirect(url_for('basket.add_item'))


@app.route('/will')
def will():
    return render_template('will.html')


if __name__ == '__main__':
    app.run()