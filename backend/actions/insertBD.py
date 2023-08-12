import mysql.connector


class DatabaseInsert:
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

    def insert_coordinator(self, name, document, email, password,user):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "INSERT INTO coordinator (name, document, email, password, user) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, document, email, password, user))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def insert_county(self, code_county, county, population, area):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "INSERT INTO county (code_county, county, population, area) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (code_county, county, population, area))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def insert_election_from_form(self, year, vote_count, political_party, county_id, coordinator_id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "INSERT INTO election (year, voteCount, politicalParty, idCounty, idCoordinator) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (year, vote_count, political_party, county_id, coordinator_id))
        self.connection.commit()
        cursor.close()
        self.close_connection()

    def insert_election(self, year, vote_count, political_party, county_id, coordinator_id):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "SELECT * FROM county WHERE code_county = %s"
        cursor.execute(sql, (county_id,))
        id_county = cursor.fetchone()
        sql = "INSERT INTO election (year, voteCount, politicalParty, idCounty, idCoordinator) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (year, vote_count, political_party, id_county[0], coordinator_id))
        self.connection.commit()
        cursor.close()
        self.close_connection()



    def insert_session(self, idCoordinador, is_logged_in, token):
        self.establish_connection()
        cursor = self.connection.cursor()
        sql = "INSERT INTO sessions (idCoordinator, is_logged_in, token) VALUES (%s, %s, %s)"
        cursor.execute(sql, (idCoordinador, is_logged_in, token))
        self.connection.commit()
        cursor.close()
        self.close_connection()
