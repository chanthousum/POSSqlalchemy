
from flask import Flask,render_template,request,session,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
# class products(db.Model):
#     producutid = db.Column('producutid', db.Integer, primary_key=True)
#     productname = db.Column(db.String(100))
#     categoryid = db.Column(db.Integer, db.ForeignKey('products.categoryid'), nullable=False)#one to many
#     def __init__(self, productname):
#         self.productname = productname
# class Categorys(db.Model):
#     categoryid = db.Column('categoryid', db.Integer, primary_key=True)
#     catetoryname = db.Column(db.String(100))
class Students(db.Model):
    __tablename__ = 'tblstudent'
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    created_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    updated_at=db.Column(db.DateTime)
    def __init__(self,name,city,addr,pin):
        self.name=name
        self.city=city
        self.addr=addr
        self.pin=pin

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    














@app.route('/')
def Index():
    db.create_all()
    # db.create_all(bind=['users'])
    return render_template("home.html")
@app.route('/student')
def StudentList():
    objstudent=Students.query.order_by(Students.name).limit(10).all()
    return render_template("student.html",student=objstudent)
@app.route('/deleteuserid/<id>')
def DeleteUserid(id):
    objstudent = Students.query.filter_by(id=id).first()
    db.session.delete(objstudent)
    db.session.commit();
    return redirect(url_for("StudentList"))
@app.route('/addstudent',methods = ['GET', 'POST'])
def AddStudent():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
                flash('Please enter all the fields', 'error')
        else:
            objstudent=Students("", "", "", "")
            objstudent.name=request.form['name'];
            objstudent.city=request.form['city']
            objstudent.addr=request.form['addr']
            objstudent.pin= request.form['pin']
            objstudent= Students(objstudent.name, objstudent.city, objstudent.addr, objstudent.pin)
            db.session.add(objstudent)
            db.session.commit()
    return redirect(url_for("StudentList"))
@app.route('/search',methods = ['GET', 'POST'])
def UserSearch():
    if request.method == 'POST':
        objstudent=Students("", "", "", "")
        objstudent.name = request.form['txt_search'];
        objstudent1=Students.query.filter_by(name=objstudent.name).all()
    return render_template("student.html",student=objstudent1)












if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=4000)

    # https: // flask - sqlalchemy.palletsprojects.com / en / 2.
    # x / queries /

    # https: // virtualzero.net / blog / connect - a - flask - app - to - a - mysql - database -
    # with-sqlalchemy - and -pymysql

    # https: // realpython.com / flask - by - example - part - 2 - postgres - sqlalchemy - and -alembic /
    # https: // realpython.com / flask - connexion - rest - api - part - 2 /