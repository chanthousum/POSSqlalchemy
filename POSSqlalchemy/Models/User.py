# class Users(db.Model):
#     __tablename__ = 'tblUser'
#     UserID = db.Column(db.Integer, primary_key=True)
#     UserName = db.Column(db.String(80))
#     Gender = db.Column(db.String(120))
#     DateOfBirth = db.Column(db.Date,)
#     Password = db.Column(db.String(120))
#     Description = db.Column(db.String(120))
#     Salary = db.Column(db.Float)
#     Phone = db.Column(db.String(120))
#     Active = db.Column(db.String(120))
#     # Position = db.Column(db.String(120),ForeignKey('tblPosition.Position'))#make relationship
#     PositionID = db.Column(db.Integer,db.ForeignKey('tblPosition.PositionID'),nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     updated_at = db.Column(db.DateTime)
# class Positions(db.Model):
#     __tablename__ = 'tblPosition'
#     PositionID=db.Column(db.Integer, primary_key=True)
#     PositionName = db.Column(db.String(120))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     updated_at = db.Column(db.DateTime)