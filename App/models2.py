from App.ext import db
import datetime
class Book(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是book。
    __tablename__ = "book"
    bookID = db.Column(db.String(7),primary_key=True,unique=True,nullable=False)
    bookName =  db.Column(db.String(20))
    bookAuthor = db.Column(db.String(20))
    bookStorage= db.Column(db.Integer)
    bookInfo = db.Column(db.String(1000))
    bookShelf = db.Column(db.Integer)
    appointment=db.relationship ('Appointment',backref='book')


class Appointment(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，appointment借阅记录。
    __tablename__ = "appointment"
    appointmentID = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    userID = db.Column(db.String(7),db.ForeignKey('client.userID'),nullable=False)
    bookID = db.Column(db.String(7),db.ForeignKey('book.bookID'),nullable=False)
    bookNum= db.Column(db.Integer,nullable=True)
    DataTime = db.Column(db.DateTime, default=datetime.datetime.now)






