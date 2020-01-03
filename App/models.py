from App.ext import db
class Client(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是client。
    __tablename__ = "client"
    userName = db.Column(db.String(20))
    userAge =  db.Column(db.Integer)
    userID = db.Column(db.String(7),primary_key=True,unique=True,nullable=False)
    userPhone= db.Column(db.String(11),unique=True,nullable=False)
    userEmail = db.Column(db.String(20),unique=True,nullable=False)
    userPassword = db.Column(db.String(20),default="000000")
    userSex=db.Column(db.CHAR(1))
    userPosition = db.Column(db.CHAR(1))
    appointment = db.relationship('Appointment', backref='client')
