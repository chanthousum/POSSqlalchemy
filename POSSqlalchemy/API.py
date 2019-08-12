from flask import Flask,json,jsonify,request
from flask_restful import Resource,Api,reqparse
from flask_sqlalchemy import SQLAlchemy
from POSSqlalchemy.Classes.User import *

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:chanthou123@localhost:5432/API_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
api=Api(app)
db=SQLAlchemy(app)
class User(Resource):
    def post(self):
        if request.method=="POST":
            objUser=Users()
            objUser.name=request.json['name']
            db.session.add(objUser)
            db.session.commit()
            db.create_all()
            message_json={'Created':'User'}
        return jsonify(message_json)
        
    # def test(self):
    #     # db.create_all()
    #     if request.method=="GET":
    #         objUser=Users.query.all()
    #         result=[]
    #         for col in objUser:
    #             dict = {}
    #             dict['id'] = col.id
    #             dict['name']=col.name
    #             result.append(dict)
    #         return  jsonify(result)
    # def get(self,id):
    #     if request.method=="GET":
    #         objUser=Users.query.filter_by(id=id).all()
    #         result=[]
    #         for col in objUser:
    #             dict = {}
    #             dict['id'] = col.id
    #             dict['name']=col.name
    #             result.append(dict)
    #
    #         return  jsonify(result)

    @app.errorhandler(404)
    def page_not_found(self):
        message_json = {'page': 'not found'}
        return jsonify(message_json),404
api.add_resource(User,"/")
# api.add_resource(User,'/post', endpoint='post')
# api.add_resource(User,'/getone/<id>', endpoint='get')


if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=4000)
    # https://flask-restful.readthedocs.io/en/latest/