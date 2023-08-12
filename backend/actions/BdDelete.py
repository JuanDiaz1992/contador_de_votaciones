import mysql.connector

class DatabaseDelete:
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

    def delete_coordinator(self, coordinator_id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM coordinator WHERE idCoordinator = %s"
        cursor.execute(sql, (coordinator_id,))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def delete_county(self, county_id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM county WHERE id = %s"
        cursor.execute(sql, (county_id,))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def delete_all_countys(self):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM county"
        cursor.execute(sql,)
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def delete_election(self, election_id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM election WHERE idElection = %s"
        cursor.execute(sql, (election_id,))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def delete_all_election(self):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM election "
        cursor.execute(sql,)
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def delete_session(self, idCoordinator):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM sessions WHERE idCoordinator = %s"
        cursor.execute(sql, (idCoordinator,))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def delete_session_by_token(self, token):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM sessions WHERE token = %s"
        cursor.execute(sql, (token,))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def closeAllSesiones(self):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "DELETE FROM sessions"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        self.close_connection()


