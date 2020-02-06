import pyodbc


class Database:

    @staticmethod
    def connect():
        conn = pyodbc.connect(
                'Driver={ODBC Driver 17 for SQL Server};'
                'Server=secretsasquatchsociety.chefvdjywstx.eu-west-2.rds.amazonaws.com,1433;'
                'Database=StoreManagement;'
                'uid=admin;'
                'pwd=letsusefirebase;')
        return conn

    @staticmethod
    def execute_sproc(query, params, cursor):
        query = """
            DECLARE @out nvarchar(max);
            EXEC %s ,@responseMessage = @out OUTPUT;
            SELECT @out AS the_output;         
            """ % query
        cursor.execute(query, params)
        return cursor.fetchall()

    @staticmethod
    def execute_query(query, cursor):
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def execute_non_query(query, cursor):
        cursor.execute(query)