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
def Login():
    if request.method == 'POST':
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=secretsasquatchsociety.chefvdjywstx.eu-west-2.rds.amazonaws.com,1433;'
                    'Database=StoreManagement;'
                    'uid=admin;'
                    'pwd=letsusefirebase;')
        sql = """
        DECLARE @out nvarchar(max);
        EXEC [usr].[UserLogin] @Email = ?, @Password= ?,@responseMessage = @out OUTPUT;
        SELECT @out AS the_output;
        """
        params = (request.form['email'], request.form['password'])
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchone()
        if "Login successful" == result[0]:
            return redirect('/home/admin')
    return redirect('/auth')
            
@app.route('/home/admin')
def admin():
    return render_template('adminArea.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

