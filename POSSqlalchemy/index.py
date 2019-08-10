
from flask import Flask, render_template, request, session, flash, redirect, url_for,jsonify,json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from json import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String,Float,DateTime,ForeignKey,create_engine,func
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base
# from POSSqlalchemy.Classes.Users import *
app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1@localhost/sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:chanthou123@localhost:5432/sqlalchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# app.config['SQLALCHEMY_BINDS']= {
#     'users':        'mysql+pymysql://root:1@localhost/sqlalchemy',
#  }#delete table and other
app.config['SECRET_KEY'] = "random string"
db=SQLAlchemy(app)
class Users(db.Model):
    __tablename__ = 'tblUser'
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(80))
    Gender = db.Column(db.String(120))
    DateOfBirth = db.Column(db.Date,)
    Password = db.Column(db.String(120))
    Description = db.Column(db.String(120))
    Salary = db.Column(db.Float)
    Phone = db.Column(db.String(120))
    Active = db.Column(db.String(120))
    # Position = db.Column(db.String(120),ForeignKey('tblPosition.Position'))#make relationship
    PositionID = db.Column(db.Integer,db.ForeignKey('tblPosition.PositionID'),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
class Positions(db.Model):
    __tablename__ = 'tblPosition'
    PositionID=db.Column(db.Integer, primary_key=True)
    PositionName = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

@app.route('/')
def Index():
    db.create_all()
    return render_template("home.html")
@app.route('/search',methods = ['GET', 'POST'])
def UserSearch():
    if request.method == 'POST':
        objstudent=Students("", "", "", "")
        objstudent.name = request.form['txt_search'];
        objstudent1=Students.query.filter_by(name=objstudent.name).all()
    return render_template("adduser.html",student=objstudent1)
    
@app.route('/AddUser',methods = ['POST'])
def AddUser():
    if request.method == 'POST':
        objUser = Users()
        objUser.UserName = request.json['UserName']
        objUser.Gender=request.json['Gender']
        objUser.PositionID = request.json['PositionID']
        db.session.add(objUser)
        db.session.commit()
        msg_json = {'message': 'User Created'}
    return jsonify(msg_json)

@app.route('/AddUser1')
def AddUser1():
    return  render_template("adduser.html")

@app.route('/GetUserAll',methods=['GET'])
def GetUserAll():
    # objUser=Users.query.order_by(Users.UserName).limit(10).all()
    if request.method=="GET":
        objUser = Users.query.all()
        output=[]
    #     for col in objUser:
    #         dict={}
    #         dict['UserID']=col.UserID
    #         dict['UserName'] = col.UserName
    #         output.append(dict)
    # return jsonify(output)
        return objUser.json()

@app.route('/GetByone/<id>',methods=['GET'])
def GetByone(id):
    if request.method=="GET":
        objUser=Users.query.filter_by(UserID=id).all()
        output=[]
        for col in objUser:
            dict={}
            dict['UserID']=col.UserID
            dict['UserName'] = col.UserName
            dict['Gender'] = col.Gender
            output.append(dict)
    return jsonify(output)

@app.route('/AddPosition',methods=['POST'])
def AddPosition():
    if request.method == 'POST':
        objPosition=Positions()
        objPosition.PositionName=request.json['PositionName']
        db.session.add(objPosition)
        db.session.commit()
        msg_json={'message':'Position Created'}
    return jsonify(msg_json)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=4000)

    # https: // flask - sqlalchemy.palletsprojects.com / en / 2.
    # x / queries /

    # https: // virtualzero.net / blog / connect - a - flask - app - to - a - mysql - database -
    # with-sqlalchemy - and -pymysql

    # https: // realpython.com / flask - by - example - part - 2 - postgres - sqlalchemy - and -alembic /
    # https: // realpython.com / flask - connexion - rest - api - part - 2 /
    # https: // medium.com / python - pandemonium / build - simple - restful - api -
    # with-python - and -flask - part - 2 - 724ebf04d12