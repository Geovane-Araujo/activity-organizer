from flask import Flask, request
from flask_cors import CORS
from service import service_login

from exceptions.exception import hubExcept

app = Flask(__name__)
CORS(app)
app.register_blueprint(hubExcept)

@app.route('/login',methods=['POST'])
def login():
    return service_login.login(request.get_json())

@app.route('/createUser',methods=['POST'])
def create_user():
    return service_login.create_user(request.get_json())


@app.route('/activitySave',methods=['POST'])
def activity_save():
    return

@app.route('/activityAll',methods=['GET'])
def activity_all():
    return 'aqui salva as atividades'


if __name__ == '__main__':
    app.run()
