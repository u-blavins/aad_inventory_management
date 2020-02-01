from flask import Flask, render_template, redirect, request, session, url_for
from models import User
from routes.auth import auth

app = Flask(__name__)
app.debug = True

app.register_blueprint(auth)

@app.route('/')
def main():
    return redirect('/auth')

@app.route('/admin')
def admin():
    return render_template('adminArea.html')

@app.route('/home')
def customer():
    return render_template('addItemToBasket.html')

@app.route('/basket')
def test():
    return render_template('basket.html')

@app.route('/will')
def will():
    return render_template('will.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)