import mysql.connector

class DatabaseModify:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def establish_connection(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def close_connection(self):
        if self.connection:
            self.connection.close()
    
    def modifySessions(self,is_logged_in,idCoordinator):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "UPDATE sessions SET is_logged_in = %s WHERE idCoordinator = %s"
        cursor.execute(sql, (is_logged_in, idCoordinator))
        self.connection.commit()
        cursor.close()
        self.close_connection()