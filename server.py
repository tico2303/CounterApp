from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///users.db')
app = Flask(__name__)
api = Api(app)

class UserName(Resource):
       def get(self, uemail):
                conn = db_connect.connect() 
                name = conn.execute("SELECT name FROM users WHERE email= '%s' "%str(uemail))
                return {"name": name.cursor.fetchall()}

class IncCount(Resource):
        def get(self, uname):
                conn = db_connect.connect() 
                conn.execute("UPDATE users SET count=count+1 WHERE name= '%s'" %str(uname)) 
                count = conn.execute("SELECT count FROM users WHERE name= '%s'" %str(uname))
                return {"name":uname,"count":count.cursor.fetchall()}

#Route1
api.add_resource(UserName, '/username/<uemail>')
#Route2
api.add_resource(IncCount, '/inccount/<uname>')



if __name__ == '__main__':
        app.run(debug=True, port=8080)
