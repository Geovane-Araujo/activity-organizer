import json
import uuid
import datetime

import mysql

from connection import py_conn
from exceptions.internal import InternalServer
from security.security import verify_session


def save(request):
    try:
        obj = request.get_json()
        id_user = verify_session(request)
        conn = py_conn.new_connection()
        currentDate = datetime.datetime.now()
        id = obj.get("id")
        sql = ""
        if(id == None or id == ''):
            sql = f"insert into note(id,id_user,title, description, created_date) values(%s,%s,%s,%s,%s)"
            id = str(uuid.uuid4())
            values = (id, id_user, obj.get("title"), obj.get("description"), currentDate.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            sql = f"UPDATE note set title=%s, description=%s where id = %s"
            values = (obj.get("title"), obj.get("description"),id)

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

        filter = obj.get('filter')
        if(filter == None):
            filter = ''
        else:
            filter = f"AND title like \'%"+filter+"%\'"

        sql = f"SELECT id, title, created_date FROM note where id_user = '{id_user}' {filter} order by title asc"
        cursor = conn.cursor()
        cursor.execute(sql)
        rs = cursor.fetchall()
        all_obj = []

        for r in rs:
            objr = {}
            objr["id"] = r[0]
            objr["title"] = r[1]
            objr["created_date"] = r[2].strftime('%d/%m/%Y %H:%M:%S')
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


        sql = "SELECT id,title, description,created_date FROM note where id = %s and id_user = %s"
        values = (id,id_user)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        rs = cursor.fetchone()
        objr = {}
        if(len(rs) > 0):
            objr["id"] = rs[0]
            objr["title"] = rs[1]
            objr["description"] = rs[2]
            objr["created_date"] = rs[3]

        return objr
    except mysql.connector.Error as err:
        raise InternalServer(err.msg)

def delete(request, id):
    try:

        conn = py_conn.new_connection()

        sql = "DELETE FROM note where id = %s"
        values = (id,)

        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        return "ok"
    except mysql.connector.Error as err:
        raise InternalServer(err.msg)