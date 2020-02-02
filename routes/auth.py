from flask import Blueprint, request, render_template, redirect, session, url_for
from utils import Database

auth = Blueprint('auth', __name__)

@auth.route('/auth')
def Auth():
    return render_template('auth.html')

@auth.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        sproc = "[usr].[UserLogin] @Email = ?, @Password= ?"
        user_email = request.form['email']
        params = (user_email, request.form['password'])
        result = Database.execute_query(sproc, params)

        if "Login successful" == result[0][0]:
            sproc = "[usr].[getUser] @Email = ?"
            session['email'] = user_email
            params = user_email
            result = Database.execute_query(sproc, params)
            is_admin = result[0][4]
            if is_admin:
                return redirect('/admin')
            else:
                return redirect('/basket')
    return redirect('/auth')

@auth.route('/auth/register', methods=['POST'])
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
        Database.execute_query(sproc, params)
    return redirect(url_for('auth.Auth'))

@auth.route('/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.Auth'))