from App.ext import db
import datetime
class Drink(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是drink。
    __tablename__ = "drink"
    dID = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    dName =  db.Column(db.String(20),unique=True,nullable=False)
    dStorage=  db.Column(db.Integer,nullable=False)
    dSell = db.Column(db.DECIMAL(7,3),nullable=False)
    dCost = db.Column(db.DECIMAL(7,3),nullable=False)


class log(db.Model):
    __tablename__ = "log"
    logID = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    logInfo= db.Column(db.String(100),unique=True,nullable=False)


class Money(db.Model):
    money=db.Column(db.DECIMAL(10,3))
    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
