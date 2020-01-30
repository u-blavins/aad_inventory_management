from flask import Flask, render_template, redirect, request, session, url_for
from utils import Database

app = Flask(__name__)
app.debug = True


@app.route('/')
@app.route('/auth')
def main():
    return render_template('auth.html')


@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        sproc = "[usr].[UserLogin] @Email = ?, @Password= ?"
        user_email = request.form['email']
        params = (user_email, request.form['password'])
        db = Database.Database()
        result = db.execute_query(sproc, params)

        if "Login successful" == result[0][0]:
            sproc = "[usr].[getUser] @Email = ?"
            params = user_email
            result = db.execute_query(sproc, params)
            is_admin = result[0][4]
            if is_admin:
                return redirect('/home/admin')
            else:
                return redirect('/home/basket')
    return redirect('/auth')


@app.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        params = (
            request.form['regEmail'],
            request.form['regPassword'],
            request.form['regFirstname'],
            request.form['regLastname'],
            request.form['departmentCode'],
            request.form['accountType'])

        sproc = """[usr].[CreateUser] @Email = ?, @Password= ?, @FirstName = ?, @LastName = ?, 
        @DepartmentCode = ?, @isStaff = ?"""
        db = Database.Database()
        db.execute_query(sproc, params)
    return redirect('/auth')


@app.route('/home/admin')
def admin():
    return render_template('adminArea.html')


@app.route('/home/basket')
def customer():
    return render_template('addItemToBasket.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
