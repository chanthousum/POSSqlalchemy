from flask import Flask,render_template,request,session,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1@localhost/sqlalchemy'
db=SQLAlchemy(app)
class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    def __init__(self,name,city,addr,pin):
        self.name=name
        self.city=city
        self.addr=addr
        self.pin=pin
@app.route('/')
def Index():
    db.create_all()
    return render_template("home.html")

@app.route('/student')
def StudentList():
    objstudent=students.query.all();
    return render_template("student.html",student=objstudent)
@app.route('/deleteuserid/<id>')
def DeleteUserid(id):
    objstudent = students.query.filter_by(id=id).first()
    db.session.delete(objstudent)
    db.session.commit();
    return redirect(url_for("StudentList"))


@app.route('/addstudent',methods = ['GET', 'POST'])
def AddStudent():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            o=students("","","","")
            o.name=request.form['name'];
            o.city=request.form['city']
            o.addr=request.form['addr']
            o.pin= request.form['pin']
            student = students(o.name,o.city,o.addr,o.pin)
            db.session.add(student)
            db.session.commit()
    return redirect(url_for("StudentList"))














if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=4000)

    # https: // flask - sqlalchemy.palletsprojects.com / en / 2.
    # x / queries /