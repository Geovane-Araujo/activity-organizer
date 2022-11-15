import mysql.connector
def new_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="adonais1_master",
        password="553322@@##",
        database="adonais1_activity_organizer"
    )
    return db

def new_connections(db):
    db = mysql.connector.connect(
        host="localhost",
        user="adonais1_master",
        password="553322@@##",
        database="adonais1_activity_organizer"
    )
    return db