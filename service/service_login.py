import json
import uuid

import mysql.connector

from connection import py_conn
from exceptions.internal import InternalServer
from exceptions.unauthorized import Unauthorized


def login(obj):
    try:

        conn   = py_conn.new_connection()

        email = obj.get("email")
        password = obj.get("password")

        sql = f"SELECT * FROM users where email = %s and password = %s";
        values = (email,password)

        cursor = conn.cursor()
        cursor.execute(sql,values)
        rs = cursor.fetchall()

        user = {
            "email": "",
            "nome": ""
        }
        if(len(rs) == 0):
            raise Unauthorized("user or password incorect")
        for r in rs:
            user["id"] = r[0]
            user["nome"] = r[1]

        return json.dumps(user)
    except mysql.connector.Error as err:
        InternalServer(err.msg)


def create_user(obj):

    try:

        conn   = py_conn.new_connection()
        name = obj.get("name")
        email = obj.get("email")
        password = obj.get("password")
        status = 1

        sql = f"insert into users(id,name, email, password, status) values(%s,%s,%s,%s,%s)"
        values = (str(uuid.uuid4()),name,email,password,status)
        cursor = conn.cursor()
        cursor.execute(sql,values)
        conn.commit()

        return "ok"
    except mysql.connector.Error as err:
        InternalServer(err.msg)
