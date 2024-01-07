import sqlite3

import mysql


def new_connections_sqlite():
    return sqlite3.connect("./security/security.db")


def new_connection():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="553322@@##",
            database="my_organizer"
        )
        return conexao

    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None