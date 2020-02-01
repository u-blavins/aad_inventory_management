import pyodbc


class Database:
    """ Database Object to execute commands """

    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=secretsasquatchsociety.chefvdjywstx.eu-west-2.rds.amazonaws.com,1433;'
        'Database=StoreManagement;'
        'uid=admin;'
        'pwd=letsusefirebase;')

    def execute_query(self, query, params):
        sql = """
            DECLARE @out nvarchar(max);
            EXEC %s ,@responseMessage = @out OUTPUT;
            SELECT @out AS the_output;         
        """ % query

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.commit()
        return result
