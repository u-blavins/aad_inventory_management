import pyodbc


def connect():
    conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=secretsasquatchsociety.chefvdjywstx.eu-west-2.rds.amazonaws.com,1433;'
            'Database=StoreManagement;'
            'uid=admin;'
            'pwd=letsusefirebase;')
    return conn


def execute_sproc(sproc, params):
    conn = connect()
    sql = """
        DECLARE @out nvarchar(max);
        EXEC %s ,@responseMessage = @out OUTPUT;
        SELECT @out AS the_output;         
        """ % sproc

    cursor = conn.cursor()
    cursor.execute(sql, params)
    if cursor is not None:
        result = cursor.fetchall()
    else:
        result = None
    cursor.commit()
    conn.close()
    return result


def execute_query(query):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    if cursor is not None:
        result = cursor.fetchall()
    else:
        result = None
    cursor.commit()
    conn.close()
    return result
