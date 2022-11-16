from flask import Flask, request
from flask_cors import CORS

from service import service_login, service_activity

from exceptions.exception import hubExcept

app = Flask(__name__)
CORS(app)
app.register_blueprint(hubExcept)

@app.route('/login',methods=['POST'])
def login():
    return service_login.login(request.get_json(), request)

@app.route('/createUser',methods=['POST'])
def create_user():
    return service_login.create_user(request.get_json())

@app.route('/activitySave',methods=['POST'])
def activity_save():
    return service_activity.save(request)

@app.route('/activityAll',methods=['POST','GET'])
def activity_all():
    return service_activity.get_all(request)

@app.route('/activityById',methods=['POST','GET'])
def activity_by_id():
    return service_activity.get_by_id(request)

@app.route('/deleteById/<id>',methods=['GET'])
def delete(id):
    return service_activity.delete(request, id)

if __name__ == '__main__':
    app.run()
