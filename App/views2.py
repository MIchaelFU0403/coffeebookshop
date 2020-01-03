from flask import *
from App.models import Client
from App.models1 import Drink
from App.models2 import Book,Appointment
from sqlalchemy import and_
from App.ext import db

blue = Blueprint('blue2',__name__)

def init_blue2(app):
    app.register_blueprint(blueprint=blue)

@blue.route('/clientPage/', methods=['GET', 'POST'])
def clientPage():
    id = session.get('userID')
    user = Client.query.filter(Client.userID == id).first()
    userdict = {
        'username': user.userName,
        'userAge': user.userAge,
        'userID': user.userID,
        'userPhone': user.userPhone,
        'userEmail': user.userEmail,
        'userPassword': user.userPassword,
        'userSex': user.userSex,
        'userPosition': user.userPosition
        }
    if request.method == 'GET':
        return render_template('clientPage.html', **userdict)

    else:
        flag=None
        userName = request.form.get('username')
        userAge = request.form.get('userAge')
        userPhone = request.form.get('userPhone')
        userEmail=request.form.get('userEmail')
        userPassword=request.form.get('userPassword')
        # 电子邮箱 unique（不可重复）
        rtn = Client.query.filter(and_(Client.userID != id,Client.userEmail == userEmail)).all()
        print(rtn)
        if rtn:
            flag=1
            return render_template('clientPage.html',flag=flag,**userdict)
        user.userEmail=userEmail

        # 手机号 unique(11位）
        if len(userPhone) !=11:
            flag=2
            return render_template('clientPage.html',flag=flag,**userdict)

        rtn = Client.query.filter(and_(Client.userID != id,Client.userPhone == userPhone)).all()
        print(rtn)
        if rtn:
            flag = 3
            return render_template('clientPage.html', flag=flag, **userdict)

        if userName.strip() is "" or userPhone.strip() is "" or userEmail.strip()is "" or userPassword.strip() is "" or userAge.strip() is "":
            flag=4
            return render_template('clientPage.html', flag=flag, **userdict)


        user.userPhone=userPhone
        #修改姓名(可重复)
        user.userName=userName
        #修改年龄 (可重复）
        user.userAge=userAge
        # 密码
        user.userPassword=userPassword
        db.session.add(user)
        db.session.commit()
        user = Client.query.filter(Client.userID == id).first()
        userdict = {
            'username': user.userName,
            'userAge': user.userAge,
            'userID': user.userID,
            'userPhone': user.userPhone,
            'userEmail': user.userEmail,
            'userPassword': user.userPassword,
            'userSex': user.userSex,
            'userPosition': user.userPosition
        }
        return render_template('clientPage.html', flag=flag, **userdict)



@blue.route('/clientDrinkLook/', methods=['GET', 'POST'])
def clientDrinkLook():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    paginate = Drink.query.paginate(page, per_page, error_out=False)

    quanbu = paginate.items

    return render_template('clientDrinkLook.html', paginate=paginate, quanbu=quanbu)

    id = session.get('userID')
    quanbu = Drink.query.all()

    if request.method == 'GET':
        return render_template('clientDrinkLook.html', quanbu=quanbu,paginate=paginate,)

    else:
        quanbu = Drink.query.all()
        return render_template('clientDrinkLook.html', quanbu=quanbu,paginate=paginate,)


@blue.route('/clientBookLook/', methods=['GET', 'POST'])
def  clientBookLook():
    # 传一个IDlist,做下拉框用

    id = session.get('userID')
    quanbu = Book.query.all()
    IDlist = []
    for bk in quanbu:
        IDlist.append(bk.bookID)
    Namelist = []
    for bk in quanbu:
        Namelist.append(bk.bookName)

    if request.method == 'GET':
        return render_template('clientBookLook.html', quanbu=quanbu, IDlist=IDlist, Namelist=Namelist)
    else:
        bookID = request.form.get('bookID')
        bookName = request.form.get('bookName')
        if bookID.strip() is "" and bookName.strip() is "":  # id，书籍名都为空 ，全部显示
            return render_template('clientBookLook.html', quanbu=quanbu, IDlist=IDlist, Namelist=Namelist)

        if bookID.strip() and bookName.strip() is "":
            quanbu = Book.query.filter(Book.bookID == bookID)  # id有 书籍名为空
            return render_template('clientBookLook.html', quanbu=quanbu, IDlist=IDlist, Namelist=Namelist)

        if bookName.strip() and bookID.strip() is "":  # id为空 书籍名有
            quanbu = Book.query.filter(Book.bookName == bookName)
            return render_template('clientBookLook.html', quanbu=quanbu, IDlist=IDlist, Namelist=Namelist)

        else:  # 应该放在前面，这里后期开发考虑功能的冗余性，可以考虑修正
            book = Book.query.filter(and_(Book.bookName == bookName, Book.bookID == bookID))
            if book:
                quanbu = book
                return render_template('clientBookLook.html', quanbu=quanbu, IDlist=IDlist, Namelist=Namelist)

            else:
                flag = 1  # 书籍名称和号不匹配
                quanbu = Book.query.all()
                return render_template('clientBookLook.html', quanbu=quanbu, IDlist=IDlist, flag=flag, Namelist=Namelist)


@blue.route('/clientBookAppointment/', methods=['GET', 'POST'])
def  clientBookAppointment():
    id = session.get('userID')
    user = Client.query.filter(Client.userID == id).first()
    userdict = {
        'username': user.userName,
        'userAge': user.userAge,
        'userID': user.userID,
        'userPhone': user.userPhone,
        'userEmail': user.userEmail,
        'userPassword': user.userPassword,
        'userSex': user.userSex,
        'userPosition': user.userPosition
    }
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 4))
    paginate = Appointment.query.filter(Appointment.userID==id).paginate(page, per_page, error_out=False)
    quanbu = paginate.items
    return render_template("clientBookAppointment.html",paginate=paginate,quanbu=quanbu,**userdict)


@blue.route('/clientBookBorrow/', methods=['GET', 'POST'])
def clientBookBorrow():
    id = session.get('userID')
    user = Client.query.filter(Client.userID == id).first()
    userdict = {
        'username': user.userName,
        'userAge': user.userAge,
        'userID': user.userID,
        'userPhone': user.userPhone,
        'userEmail': user.userEmail,
        'userPassword': user.userPassword,
        'userSex': user.userSex,
        'userPosition': user.userPosition
    }
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 3))
    paginate = Book.query.paginate(page, per_page, error_out=False)
    quanbu = paginate.items
    if request.method == 'GET':
        return render_template("clientBookBorrow.html", paginate=paginate, quanbu=quanbu, **userdict)
    else:
        bookID = request.form.get('bookID')
        bookborrowNum = request.form.get('bookborrowNum')
        if bookborrowNum.strip()=="": #输入借阅数为空
            flag=4
            return render_template("clientBookBorrow.html", paginate=paginate, quanbu=quanbu, **userdict, flag=flag)

        book =Book.query.filter(Book.bookID==bookID).first()
        if book :
            if int(bookborrowNum)>0 and int(bookborrowNum)<book.bookStorage:
                ap=Appointment()
                ap.bookID=bookID
                ap.userID=id
                book.bookStorage -= int(bookborrowNum)
                if book.bookStorage==0:
                    db.session.delete(book)
                elif book.bookStorage>0:
                    db.session.add(book)
                ap.bookNum=int(bookborrowNum)
                db.session.add(ap)
                db.session.commit()
                flag=1#借阅成功
                return render_template("clientBookBorrow.html", paginate=paginate, quanbu=quanbu, **userdict,flag=flag)

            if int(bookborrowNum)==book.bookStorage:
                flag=5 #请至少保留一本书留在店里为别的用户观看
                return render_template("clientBookBorrow.html", paginate=paginate, quanbu=quanbu, **userdict,flag=flag)
            else:
                flag=2#输入有误或库存不足
                return render_template("clientBookBorrow.html", paginate=paginate, quanbu=quanbu, **userdict,flag=flag)
        else:
            flag=3 #找不到要借阅书籍的编号
            return render_template("clientBookBorrow.html", paginate=paginate, quanbu=quanbu, **userdict, flag=flag)


