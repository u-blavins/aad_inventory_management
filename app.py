from flask import Flask, render_template, redirect, request, session, url_for
import pyodbc
import os

app = Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/auth')
def main():
    return render_template('auth.html')

@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=secretsasquatchsociety.chefvdjywstx.eu-west-2.rds.amazonaws.com,1433;'
            'Database=StoreManagement;'
            'uid=admin;'
            'pwd=letsusefirebase;')
        sql = """
        DECLARE @out nvarchar(max);
        EXEC [usr].[UserLogin] @Email = ?, @Password= ?,@responseMessage = @out OUTPUT;
        SELECT @out AS the_output;
        """
        userEmail = request.form['email']
        params = (userEmail, request.form['password'])
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchone()
        if "Login successful" == result[0]:
            sql = "EXEC [usr].[getUser] @Email = ?"
            params = userEmail
            cursor.execute(sql, params)
            getRow = cursor.fetchone()
            isAdmin = getRow[4]
            conn.close()
            if isAdmin:
                return redirect('/home/admin')
            else:
                return redirect('/home/basket')

    conn.close()
    return redirect('/auth')

@app.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=secretsasquatchsociety.chefvdjywstx.eu-west-2.rds.amazonaws.com,1433;'
            'Database=StoreManagement;'
            'uid=admin;'
            'pwd=letsusefirebase;')
        sql = """
        DECLARE @out nvarchar(max);
        EXEC [usr].[CreateUser] @Email = ?, @Password= ?, @FirstName = ?, @LastName = ?, 
        @DepartmentCode = ?, @isStaff = ?, @responseMessage = @out OUTPUT;
        SELECT @out AS the_output;
        """
        params = (
            request.form['regEmail'],
            request.form['regPassword'],
            request.form['regFirstname'],
            request.form['regLastname'],
            request.form['departmentCode'],
            request.form['accountType'])
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchone()
        if "Success" == result[0]:
            conn.commit()
            conn.close()
        else:
            conn.close()
    return redirect('/auth')

@app.route('/home/admin')
def admin():
    return render_template('adminArea.html')

@app.route('/home/basket')
def customer():
    return render_template('addItemToBasket.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

