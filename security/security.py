import json
import sqlite3
import string
import random
import base64
from datetime import datetime, timedelta

from connection.py_conn import new_connections_sqlite
from exceptions.internal import InternalServer
from exceptions.unauthorized import Unauthorized


def encode():
    token = ""
    for x in range(1):
        token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))
    return token

def save_data_access(obj, request, iduser):
    try:
        cnn = new_connections_sqlite()

        delete_old_tokens(cnn,iduser)
        hora_atual = datetime.now() + timedelta(hours=10)

        sql = f"insert into users_access(token, id_usuario, expiration, ip_session) values(?,?,?,?)"
        values = (obj['token'],iduser,str(hora_atual),request.remote_addr)
        cursor = cnn.cursor()
        cursor.execute(sql,values)
        cnn.commit()
    except Exception as err:
        raise InternalServer(json.dumps(err.args))

def delete_old_tokens(cnn, iduser):

    sql = "DELETE FROM users_access where id_usuario = ?"
    values = (iduser,)
    cursor = cnn.cursor()
    cursor.execute(sql, values)
    cnn.commit()

def verify_session(request):
    try:
        cnn = new_connections_sqlite()
        token = request.headers.get("Authorization")
        token = token.replace("Bearer ","")
        sql = f"SELECT id_usuario,expiration  FROM users_access where token = ?";
        values = (token,)
        cursor = cnn.cursor()
        cursor.execute(sql, values)
        rs = cursor.fetchall()

        if(len(rs) == 0):
            raise Unauthorized("invalid token or expired")
        id_user = ''
        expiration = datetime.now()
        for r in rs:
            id_user = r[0]
            expiration = r[1]

        if(datetime.strptime(expiration,'%Y-%m-%d %H:%M:%S.%f')<datetime.now()):
            raise Unauthorized("invalid token or expired")

        return id_user
    except sqlite3.Error as err:
        raise InternalServer(json.dumps(err.args))