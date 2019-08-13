from POSSqlalchemy.API import *
class Users(db.Model):
    __tablename__ = 'tblUser'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120))
    # gender=db.Column(db.String(120))

# class Positions(db.Model):
#     __tablename__ = 'tblPosition'
#     position_id=db.Column(db.Integer, primary_key=True)
#     position_name=db.Column(db.String(120))
