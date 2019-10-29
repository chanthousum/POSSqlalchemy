from flask import Flask, render_template, request, session, flash, redirect, url_for,jsonify,json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from sqlalchemy import Column, Integer, String,Float,DateTime,ForeignKey,create_engine,func
# from sqlalchemy.orm import relationship,backref
# from sqlalchemy.ext.declarative import declarative_base
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

@app.route('/login',methods=['POST'])
def Login():
    try:
        error = None
        if request.method == "POST":
            objUser = Users()
            objUser.UserName = request.form['txt_username']
            objUser.Password = request.form['txt_password']
            # objUser = Users.query.filter_by(UserName=objUser.UserName,Password=objUser.Password).first()
            objUser=db.session.query(Users.UserName,Users.Password,Positions.PositionID,Positions.PositionName).filter(Users.PositionID==Positions.PositionID).filter_by(UserName=objUser.UserName,Password=objUser.Password).first()
            if not objUser:
                error="Username and Password is invalid"
                return render_template("login_frm.html",error=error)
            else:
                session['username']=objUser.UserName
                session['PositionName'] = objUser.PositionName
                return render_template("index.html",username= session['username'],PositionName=session['PositionName'])
    except Exception as ex:
        return render_template("Error.html",errre_message=ex)

@app.route('/logout')
def LogOut():
    session.pop('username',None)
    return redirect(url_for("Index"))
@app.route('/home')
def Index():
   db.create_all()
   return render_template("login_frm.html")
app.add_url_rule("/","home",Index)

@app.route('/userlist',methods=['GET'])
def UserList():
    # userlist=Users.query.order_by(Users.UserName).all()
    userlist=db.session.query(Users.UserID,Users.UserName,Users.Gender,Positions.PositionName).filter(Users.PositionID==Positions.PositionID)#get data by file table
    return render_template("users/userlist.html",userlists=userlist)

@app.route('/adduser')
def AddUser():
    position=Positions.query.all()
    return render_template("users/adduser_frm.html",positions=position)

@app.route('/usercreate',methods=['POST'])
def Save():
    try:
        if request.method == "POST":
            objUser = Users()
            objUser.UserName= request.form['txt_username']
            objUser.Gender = request.form['ddlgender']
            objUser.DateOfBirth = request.form['txt_date']
            objUser.Password = request.form['txt_password']
            objUser.Description = request.form['txt_description']
            objUser.Salary = request.form['txt_salary']
            objUser.Phone = request.form['txt_phone']
            objUser.Active = request.form['ddlactive']
            objUser.PositionID = request.form['ddlposition']
            db.session.add(objUser)
            db.session.commit()
            flash("Created User")
        return redirect(url_for("AddUser"))
    except Exception as ex:
        return render_template("Error.html",errre_message=ex)

@app.route('/userupdate/<id>',methods=['POST'])
def UserUpdate(id):
    try:
        if request.method == "POST":
            objUser = Users.query.filter_by(UserID=id).first()  # get one record
            objUser.UserName = request.form['txt_username']
            objUser.Gender = request.form['ddlgender']
            objUser.DateOfBirth = request.form['txt_date']
            objUser.Password = request.form['txt_password']
            objUser.Description = request.form['txt_description']
            objUser.Salary = request.form['txt_salary']
            objUser.Phone = request.form['txt_phone']
            objUser.Active = request.form['ddlactive']
            objUser.PositionID = request.form['ddlposition']
            objUser.updated_at=datetime.now()
            db.session.add(objUser)
            db.session.commit()
            if db.session.has_object(objUser):
                flash("Updated User")
                return redirect("/useredit/" + id + "")



    except Exception as ex:
        return render_template("Error.html", errre_message=ex)


@app.route('/useredit/<id>',methods=['GET'])
def UserEdit(id):
    userlist=Users.query.filter_by(UserID=id).all()
    position = Positions.query.all()
    return render_template("users/edituser_frm.html",userlists=userlist,positions=position,username=session['username'])

@app.route('/userdelete/<id>',methods=['GET'])
def UserDelete(id):
    objUser=Users.query.filter_by(UserID=id).first()
    db.session.delete(objUser)
    db.session.commit()
    return redirect(url_for("UserList"))

# ==========================================Position
@app.route('/SavePosition',methods=['POST'])
def SavePosition():
    if request.method == 'POST':
        objPosition=Positions()
        objPosition.PositionName=request.form['txt_position_name']
        db.session.add(objPosition)
        db.session.commit()
        flash("Created Position")
    return redirect(url_for("AddPostionForm"))

@app.route('/UpdatePosition/<id>',methods=['POST'])
def UpdatePosition(id):
    if request.method == 'POST':
        objPosition=Positions.query.filter_by(PositionID=id).first()
        objPosition.PositionName=request.form['txt_position_name']
        db.session.add(objPosition)
        db.session.commit()
        flash("Position Updated")
    return redirect("/PositionEdit/"+id +"")

@app.route('/AddPostionForm')
def AddPostionForm():
    return render_template("users/add_position_frm.html")
@app.route('/positionlist')
def PositionList():
    positionlist = Positions.query.all()
    return render_template("users/position_list.html", positionlists=positionlist,username=session['username'])

@app.route('/PositionEdit/<id>',methods=['GET'])
def PositionEdit(id):
    positionlist=Positions.query.filter_by(PositionID=id).all()
    return render_template("users/edit_position_frm.html",positionlists=positionlist,username=session['username'])





@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404



if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=5000)

    # https: // flask - sqlalchemy.palletsprojects.com / en / 2.
    # x / queries /

    # https: // virtualzero.net / blog / connect - a - flask - app - to - a - mysql - database -
    # with-sqlalchemy - and -pymysql

    # https: // realpython.com / flask - by - example - part - 2 - postgres - sqlalchemy - and -alembic /
    # https: // realpython.com / flask - connexion - rest - api - part - 2 /
    # https: // medium.com / python - pandemonium / build - simple - restful - api -
    # with-python - and -flask - part - 2 - 724ebf04d12d
    # https: // freecoursesite.com /?s = Web + API + Development +
    # with+Flask