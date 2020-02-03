from flask import Flask, render_template, redirect, request, session, url_for
from models import User
from routes.auth import auth
from routes.admin import admin

app = Flask(__name__)
app.debug = True

# Random os.urandom(16) secret key
app.secret_key = b'\x9a\xac\xea\x9e\xe9\xbbN\x1d\xa5\xb4\x1f\x17\xd3\xdd\x96O'

app.register_blueprint(auth)
app.register_blueprint(admin)


@app.route('/')
def main():
    return redirect('/auth')


@app.route('/home')
def customer():
    if 'is_admin' in session:
        if session['is_admin'] != None:
            if session['is_admin'] == True:
                return redirect('/admin')
    return redirect('/basket')


@app.route('/basket')
def test():
    if session.get('email') is None:
        return redirect(url_for('auth.Auth'))
    return render_template('basket.html')


@app.route('/will')
def will():
    return render_template('will.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')