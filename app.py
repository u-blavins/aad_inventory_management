from flask import Flask, render_template, redirect, request, session, url_for
from utils.Database import execute_query as execute_query

app = Flask(__name__)
app.debug = True


@app.route('/')
def main():
    return redirect('/auth')

@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/auth/login', methods=['POST'])
def login():
def login():
    if request.method == 'POST':
        sproc = "[usr].[UserLogin] @Email = ?, @Password= ?"
        user_email = request.form['email']
        params = (user_email, request.form['password'])
        result = execute_query(sproc, params)

        if "Login successful" == result[0][0]:
            sproc = "[usr].[getUser] @Email = ?"
            params = user_email
            result = execute_query(sproc, params)
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
        execute_query(sproc, params)
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

@app.route('/logout')
def logout():
    return redirect('/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)