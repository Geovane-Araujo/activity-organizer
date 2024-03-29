import json
import uuid
from datetime import datetime

import mysql

from connection import py_conn
from exceptions.internal import InternalServer
from security.security import verify_session


def save(request):
    try:
        obj = request.get_json()
        id_user = verify_session(request)

        conn = py_conn.new_connection()

        data = obj.get("data")
        title = obj.get("title")
        description = obj.get("description")
        status = obj.get("status")
        id = obj.get("id")

        sql = ""
        if(id == None or id == ''):
            sql = f"insert into activity(id,id_user,data, title, description, status) values(%s,%s,%s,%s,%s,%s)"
            id = str(uuid.uuid4())
            values = (id, id_user, data, title, description, status)
        else:
            sql = f"UPDATE activity set data=%s, title=%s, description=%s, status=%s where id = %s"
            values = (data, title, description, status,id)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()

        return "ok"
    except mysql.connector.Error as err:
        raise InternalServer(err.msg)


def get_all(request):
    try:
        obj = request.get_json()
        id_user = verify_session(request)

        conn = py_conn.new_connection()

        data_start = obj.get("dataStart")
        data_start = datetime.strptime(data_start,'%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')

        data_end = obj.get("dataEnd")
        data_end = datetime.strptime(data_end, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')

        sql = "SELECT * FROM activity where data between %s and %s and id_user = %s order by data asc"
        values = (str(data_start) + " 00:00:00",str(data_end) + " 23:59:59",id_user)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        rs = cursor.fetchall()
        all_obj = []

        for r in rs:
            objr = {}
            objr["id"] = r[0]
            objr["id_user"] = r[1]
            objr["data"] = r[2].strftime('%Y-%m-%d %H:%M:%S.%f')
            objr["title"] = r[3]
            objr["description"] = r[4] if len(r[4]) < 50 else r[4][0:50] + "..."
            objr["status"] = r[5]
            all_obj.append(objr)

        return all_obj
    except mysql.connector.Error as err:
        raise InternalServer(err.msg)

def get_by_id(request):
    try:
        obj = request.get_json()
        id_user = verify_session(request)

        conn = py_conn.new_connection()

        id = obj.get("id")


        sql = "SELECT * FROM activity where id = %s and id_user = %s"
        values = (id,id_user)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        rs = cursor.fetchone()


        objr = {}
        objr["id"] = rs[0]
        objr["id_user"] = rs[1]
        objr["data"] = rs[2].strftime('%Y-%m-%d %H:%M:%S.%f')
        objr["title"] = rs[3]
        objr["description"] = rs[4]
        objr["status"] = rs[5]


        return objr
    except mysql.connector.Error as err:
        raise InternalServer(err.msg)

def delete(request, id):
    try:

        conn = py_conn.new_connection()


        sql = "DELETE FROM activity where id = %s"
        values = (id,)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()


        return "ok"
    except mysql.connector.Error as err:
        raise InternalServer(err.msg)