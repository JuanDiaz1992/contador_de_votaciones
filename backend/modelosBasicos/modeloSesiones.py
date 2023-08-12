import mysql.connector

def establish_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='3118514322s',
        database='voting'
    )
    return connection

def create_sessions_table():
    connection = establish_connection()
    cursor = connection.cursor()
    
    sql = """
    CREATE TABLE sessions (
        idCoordinator INT PRIMARY KEY,
        is_logged_in BOOLEAN,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        token  VARCHAR(2000),
        FOREIGN KEY (idCoordinator) REFERENCES coordinator(idCoordinator)
    )
    """

    
    cursor.execute(sql)
    
    cursor.close()
    connection.close()

# Llama a la función para crear la tabla
create_sessions_table()
