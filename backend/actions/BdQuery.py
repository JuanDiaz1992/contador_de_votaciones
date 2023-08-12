import mysql.connector

class DatabaseQuery:
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

    def get_county_by_name(self, county_name):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM county WHERE county = %s"
        cursor.execute(sql, (county_name,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result
    
    def get_county_by_code_county(self, code_county):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM county WHERE code_county = %s"
        cursor.execute(sql, (code_county,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result
    
    def get_all_countys(self):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM county"
        cursor.execute(sql,())
        result = cursor.fetchall()
        cursor.close()
        self.close_connection()
        return result


    def get_coordinator_by_name(self, user):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM coordinator WHERE user = %s"
        cursor.execute(sql, (user,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result
    
    def get_coordinator_by_id(self, id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM coordinator WHERE idCoordinator = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result
    
    def get_coordinator_by_password_and_name(self, password, user):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM coordinator WHERE password = %s AND user = %s"
        cursor.execute(sql, (password, user))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result

    def get_election_by_id(self, election_id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM election WHERE idElection = %s"
        cursor.execute(sql, (election_id,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result
    
    def get_all_election(self):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM election"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        self.close_connection()
        return results




    def get_session_by_id(self, id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM sessions WHERE idCoordinator = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result
    
    def get_session_active_by_token(self, token):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM sessions WHERE token = %s"
        cursor.execute(sql, (token,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        return result
