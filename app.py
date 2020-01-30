from flask import Flask, render_template, redirect, request, session, url_for
import pypyodbc
import os

app = Flask(__name__)
app.debug = True


# try:
#     #creating connection Object which will contain SQL Server Connection
#     connection = pypyodbc.connect('')
#     print("Connected.")
#     #closing connection
#     connection.close()
# except Exception as ex:
#     print(ex)

@app.route('/')
def main():
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')