from flask import *
from App.models import Client
from App.models1 import Drink,Money
from App.models2 import Book,Appointment
from sqlalchemy import and_,or_
from App.ext import db



blue = Blueprint('blue1',__name__)

def init_blue1(app):
    app.register_blueprint(blueprint=blue)

@blue.route('/manageSearch/', methods=['GET', 'POST'])
def manageSearch():
    quanbu = Client.query.all()

    if request.method == 'POST':
        userName=request.form.get('userName')
        userID=request.form.get('userID')
        userSex=request.form.get('userSex')
        userPosition=request.form.get('userPosition')

        if  userID:
            quanbu = Client.query.filter(Client.userID == userID)
            return render_template('manageSearch.html', quanbu=quanbu)

        if userName:
             quanbu = Client.query.filter(Client.userName.like("%"+userName+"%"))
             return render_template('manageSearch.html', quanbu=quanbu)

        if userSex:
            quanbu= Client.query.filter(Client.userSex==userSex)
            return render_template('manageSearch.html', quanbu=quanbu)

        if userPosition:
            quanbu = Client.query.filter(Client.userPosition==userPosition)
            return render_template('manageSearch.html', quanbu=quanbu)




    quanbu = Client.query.all()
    return render_template('manageSearch.html', quanbu=quanbu)


@blue.route('/manageUpdate/', methods=['GET', 'POST'])
def manageUpdate():
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
        return render_template('manageUpdate.html', **userdict)

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
            return render_template('manageUpdate.html',flag=flag,**userdict)
        user.userEmail=userEmail

        # 手机号 unique(11位）
        if len(userPhone) !=11:
            flag=2
            return render_template('manageUpdate.html',flag=flag,**userdict)

        rtn = Client.query.filter(and_(Client.userID != id,Client.userPhone == userPhone)).all()
        print(rtn)
        if rtn:
            flag = 3
            return render_template('manageUpdate.html', flag=flag, **userdict)

        if userName.strip() is "" or userPhone.strip() is "" or userEmail.strip()is "" or userPassword.strip() is "" or userAge.strip() is "":
            flag=4
            return render_template('manageUpdate.html', flag=flag, **userdict)

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
        return render_template('manageUpdate.html', flag=flag, **userdict)


@blue.route('/manageDelete/',methods=['GET', 'POST'])
def manageDelete():
    id = session.get('userID')
    quanbu = Client.query.all()

    if request.method == 'GET':
        return render_template('manageDelete.html' , quanbu=quanbu)

    else:
        flag=None
        userID = request.form.get('userID')
        if userID==id :
            # 输入的值不能是自己
            flag=1

            return render_template('manageDelete.html',quanbu=quanbu ,flag=flag)
        user=Client.query.filter(Client.userID==int(userID)).first()
        if user:
            ap=Appointment.query.filter(Appointment.userID==int(userID)).first()
            if ap:
                flag=2
                # 该用户正在借阅
                return render_template('manageDelete.html', quanbu=quanbu, flag=flag)

            else:
                flag=3
                # 删除成功
                db.session.delete(user)
                db.session.commit()
                quanbu = Client.query.all()
                return render_template('manageDelete.html', quanbu=quanbu, flag=flag)

        else:
            flag=4
            # 未找到该用户
            return render_template('manageDelete.html',quanbu=quanbu, flag=flag)




@blue.route('/bookInsert/', methods=['GET', 'POST'])
def bookInsert():
    if request.method == 'GET':
        return render_template('bookInsert.html')
    else:
        bookID=request.form.get('bookID')
        bookName=request.form.get('bookName')
        bookAuthor=request.form.get('bookAuthor')
        bookStorage=request.form.get('bookStorage')
        bookInfo=request.form.get('bookInfo')
        bookShelf=request.form.get('bookShelf')

        bookdict={
            'bookID':bookID,
            'bookName':bookName,
            'bookAuthor':bookAuthor,
            'bookStorage':bookStorage,
            'bookInfo':bookInfo,
            'bookShelf':bookShelf
                }
        book = Book.query.filter(Book.bookID == bookID).first()
        if book:
            flag = 1
            #插入编号已经有图书
            return render_template("bookInsert.html", flag=flag, **bookdict)

        if bookShelf.strip() is "" or bookStorage.strip() is ""or len(bookAuthor)==0 or len(bookName)==0 or len(bookID)==0 or len(bookInfo)>1000:
            flag = 2

            return render_template("bookInsert.html", flag=flag, **bookdict)
        else:
            bk=Book()
            bk.bookID=bookID
            bk.bookName=bookName
            bk.bookAuthor=bookAuthor
            bk.bookInfo=bookInfo
            bk.bookStorage=bookStorage
            bk.bookShelf=bookShelf
            db.session.add(bk)
            db.session.commit()
            flag=3

            return render_template("bookInsert.html", flag=flag)


@blue.route('/bookUpdate/', methods=['GET', 'POST'])
def bookUpdate():
    id = session.get('userID')
    quanbu = Book.query.all()
    IDlist = []
    for bk in quanbu:
        IDlist.append(bk.bookID)
    if request.method == 'GET':
        return render_template("bookUpdate.html", quanbu=quanbu,IDlist=IDlist)
    else:
        bookID = request.form.get('bookID')

        bookdict = {
            'bookID': bookID,
        }

        if bookID.strip() is "" or None: #ID为空或空格
            return render_template("bookUpdate.html", quanbu=quanbu, **bookdict,IDlist=IDlist)

        if bookID.strip():
            book = Book.query.filter(Book.bookID==bookID).first()
            if book:  # book存在，成功跳转
                session['bookID'] = book.bookID
                session.permanent = True
                return redirect(url_for('blue1.bookUpdate2'))

            else:#book不存在
                flag=1
                return render_template("bookUpdate.html", quanbu=quanbu, flag=flag, **bookdict,IDlist=IDlist)



@blue.route('/bookUpdate2/', methods=['GET', 'POST'])
def bookUpdate2():
        bookID = session.get('bookID')
        book = Book.query.filter(Book.bookID == bookID).first()
        bookdict = {
            'bookID':book.bookID,
            'bookName':book.bookName,
            'bookAuthor': book.bookAuthor,
            'bookStorage':book.bookStorage,
            'bookInfo': book.bookInfo,
            'bookShelf':book.bookShelf
        }
        if request.method == 'GET':
            return render_template("bookUpdate2.html",**bookdict)
        else:
            bookID = request.form.get('bookID')
            bookName = request.form.get('bookName')
            bookAuthor = request.form.get('bookAuthor')
            bookStorage = request.form.get('bookStorage')
            bookInfo = request.form.get('bookInfo')
            bookShelf = request.form.get('bookShelf')

            if bookShelf.strip()=="" or bookInfo.strip()=="" or bookStorage.strip()==""or bookAuthor.strip()=="" or bookName.strip()=="":
                flag=1 #相关信息不能为空
                return render_template("bookUpdate2.html", **bookdict, flag=flag)

            #传入时就一定存在且卡死不变

            book.bookName=bookName
            book.bookAuthor = bookAuthor
            book.bookStorage=bookStorage
            book.bookInfo=bookInfo
            book.bookShelf=bookShelf
            db.session.add(book)
            db.session.commit()
            flag=2 #修改成功
            bookdict = {
                'bookID': book.bookID,
                'bookName': book.bookName,
                'bookAuthor': book.bookAuthor,
                'bookStorage': book.bookStorage,
                'bookInfo': book.bookInfo,
                'bookShelf': book.bookShelf
            }
            return render_template("bookUpdate2.html", **bookdict, flag=flag)




@blue.route('/bookSearch/', methods=['GET', 'POST'])
def bookSearch():
    #传一个IDlist,做下拉框用

    id = session.get('userID')
    quanbu = Book.query.all()
    IDlist=[]
    for bk in quanbu:
        IDlist.append(bk.bookID)
    Namelist=[]
    for bk in quanbu:
        Namelist.append(bk.bookName)

    if request.method == 'GET':
        return render_template('bookSearch.html', quanbu=quanbu,IDlist=IDlist,Namelist=Namelist)
    else:
        bookID = request.form.get('bookID')
        bookName = request.form.get('bookName')
        if bookID.strip() is "" and bookName.strip() is "": #id，书籍名都为空 ，全部显示
            return render_template('bookSearch.html', quanbu=quanbu,IDlist=IDlist,Namelist=Namelist)

        if bookID.strip()  and bookName.strip()is "":
            quanbu=Book.query.filter(Book.bookID == bookID) #id有 书籍名为空
            return render_template('bookSearch.html', quanbu=quanbu,IDlist=IDlist,Namelist=Namelist)


        if bookName.strip()  and bookID.strip() is "":  #id为空 书籍名有
            quanbu = Book.query.filter(Book.bookName == bookName)
            return render_template('bookSearch.html', quanbu=quanbu,IDlist=IDlist,Namelist=Namelist)

        else:   #应该放在前面，这里后期开发考虑功能的冗余性，可以考虑修正
            book= Book.query.filter(and_(Book.bookName == bookName,Book.bookID == bookID))
            if book:
                quanbu=book
                return render_template('bookSearch.html', quanbu=quanbu, IDlist=IDlist,Namelist=Namelist)

            else:
                flag = 1 #书籍名称和号不匹配
                quanbu = Book.query.all()
                return render_template('bookSearch.html', quanbu=quanbu, IDlist=IDlist,flag=flag,Namelist=Namelist)


@blue.route('/bookDelete/',methods=['GET', 'POST'])
def bookDelete():

    id = session.get('userID')
    quanbu = Book.query.all()
    if request.method == 'GET':
        return render_template('bookDelete.html', quanbu=quanbu)

    else:

        bookID = request.form.get('bookID')
        bdict={
            'bookID':bookID
        }
        book = Book.query.filter(Book.bookID == bookID).first()

        if book:
            ap=Appointment.query.filter(Appointment.bookID == int(bookID)).first()
            if ap:
                flag = 1
                return render_template('bookDelete.html', quanbu=quanbu, flag=flag,**bdict)


            else:
                flag=2
                db.session.delete(book)
                db.session.commit()
                quanbu = Book.query.all()
                return render_template('bookDelete.html', quanbu=quanbu, flag=flag, **bdict)

        else:
            flag = 3
            quanbu = Book.query.all()
            return render_template('bookDelete.html', quanbu=quanbu, flag=flag,**bdict)





@blue.route('/drinkInsert/', methods=['GET', 'POST'])
def drinkInsert():
    if request.method == 'GET':
        return render_template("drinkInsert.html")
    else:
        dID = request.form.get('dID')
        dName =  request.form.get('dName')
        dStorage=  request.form.get('dStorage')
        dSell = request.form.get('dSell')
        dCost =request.form.get('dCost')
        ddcit={
            'dID':dID,
            'dName':dName,
            'dStorage':dStorage,
            'dSell':dSell,
            'dCost':dCost
        }
        drink = Drink.query.filter(or_(Drink.dID == dID,Drink.dName==dName)).first()
        if drink:
            flag = 1
            # 插入编号已经有饮料dSell>=dCost 字符串转化为数字
            return render_template("drinkInsert.html", flag=flag, **ddcit)
        if dName.strip() is ""or dID.strip() is "" or float(dSell)<float(dCost) or int(dStorage)<=0:
            flag = 2
            return render_template("drinkInsert.html", flag=flag, **ddcit)
        else:
            dk=Drink()
            dk.dName=dName
            dk.dID=dID
            dk.dCost=dCost
            dk.dSell=dSell
            dk.dStorage=dStorage
            db.session.add(dk)
            db.session.commit()
            flag = 3
            return render_template("drinkInsert.html", flag=flag)

    return render_template("drinkInsert.html")



@blue.route('/drinkUpdate/', methods=['GET', 'POST'])
def drinkUpdate():
    id = session.get('userID')
    quanbu = Drink.query.all()
    if request.method=='GET':
        return render_template("drinkUpdate.html",quanbu=quanbu)
    else:
        dID = request.form.get('dID')
        dName = request.form.get('dName')  #记录输入值
        ddict={
            'dID':dID,
            'dName':dName
        }
        if dID and dName:       #如果两个都输入了
            dk = Drink.query.filter(and_(Drink.dID == dID,Drink.dName == dName)).first()
            if dk:  # 成功跳转
                session['dID'] = dk.dID
                session.permanent = True
                return redirect(url_for('blue1.drinkUpdate2'))

            else:
                flag = 1  # 输入的ID与名称不匹配
                return render_template("drinkUpdate.html", quanbu=quanbu, flag=flag, **ddict)

        if dID.strip()  and dName.strip() is "":  #有ID无名称
            dk=Drink.query.filter(Drink.dID == dID).first() #去搜索该ID对应的饮料
            if dk:#如果有
                session['dID'] = dk.dID
                session.permanent = True
                return redirect(url_for('blue1.drinkUpdate2'))

            else:
                flag=2 #输入的ID值数据库中查找不到
                return render_template("drinkUpdate.html", quanbu=quanbu, flag=flag, **ddict)
                #回到当前更改1页面


        if dName.strip() and dID.strip() is "": #有名称无ID
            dk = Drink.query.filter(Drink.dName == dName).first()#去搜索该名称对应的饮料
            if dk: #如果有
                session['dName'] = dk.dName
                session.permanent = True
                return redirect(url_for('blue1.drinkUpdate2'))

            else:
                flag=3
                return render_template("drinkUpdate.html", quanbu=quanbu, flag=flag, **ddict)
                # 回到当前更改1页面


        else:
            flag=4

        return render_template("drinkUpdate.html", quanbu=quanbu, flag=flag, **ddict)




@blue.route('/drinkUpdate2/', methods=['GET', 'POST'])
def drinkUpdate2():
        dID = session.get('dID')
        dName=session.get('dName')
        drink = Drink .query.filter(or_(Drink.dID == dID,Drink.dName == dName)).first()
        ddcit = {
            'dID': drink.dID,#固定部分
            'dName': drink.dName, #固定部分
            'dStorage': drink.dStorage,
            'dSell': drink.dSell,
            'dCost': drink.dCost
        }
        if request.method == 'GET':
            return render_template("drinkUpdate2.html",**ddcit)
        else:
            dID = request.form.get('dID')
            dName = request.form.get('dName')
            dStorage = request.form.get('dStorage')
            dSell = request.form.get('dSell')
            dCost = request.form.get('dCost')

            drink=Drink.query.filter(Drink.dID==dID).first()
            if dSell<dCost:
                flag=1 #售价不能低于成本
                return render_template("drinkUpdate2.html", **ddcit,flag=flag)
            if dStorage.strip()=="" or dSell.strip()=="" or dCost.strip()=="":
                flag=2 #相关信息不能为空
                return render_template("drinkUpdate2.html", **ddcit, flag=flag)

            #传入时就一定存在且卡死不变
            drink.dSell=dSell
            drink.dCost=dCost
            drink.dStorage=dStorage
            db.session.add(drink)
            db.session.commit()
            flag=3 #修改成功
            ddcit = {
                'dID': drink.dID,  # 固定部分
                'dName': drink.dName,  # 固定部分
                'dStorage': drink.dStorage,
                'dSell': drink.dSell,
                'dCost':drink. dCost
            }
            return render_template("drinkUpdate2.html", **ddcit, flag=flag)


@blue.route('/drinkSearch/', methods=['GET', 'POST'])
def drinkSearch():
    id = session.get('userID')
    quanbu = Drink.query.all()

    if request.method == 'GET':
        return render_template('drinkSearch.html', quanbu=quanbu)
    else:
        dID = request.form.get('dID')
        dName = request.form.get('dName')
        dStorage = request.form.get('dStorage')
        dSell = request.form.get('dSell')
        dCost = request.form.get('dCost')
        if dID:
            quanbu =Drink.query.filter(Drink.dID == dID)
            return render_template('drinkSearch.html', quanbu=quanbu)
        if dName:
            quanbu = Drink.query.filter(Drink.dName == dName)
            return render_template('drinkSearch.html', quanbu=quanbu)
        if dStorage:
            quanbu = Drink.query.filter(Drink.dStorage == dStorage)
            return render_template('drinkSearch.html', quanbu=quanbu)
        if dSell:
            quanbu = Drink.query.filter(Drink.dSell == dSell)
            return render_template('drinkSearch.html', quanbu=quanbu)
        if dCost:
            quanbu = Drink.query.filter(Drink.dCost == dCost)
            return render_template('drinkSearch.html', quanbu=quanbu)

        else:
            quanbu = Drink.query.all()
            return render_template('drinkSearch.html', quanbu=quanbu)


@blue.route('/drinkDelete/',methods=['GET', 'POST'])
def drinkDelete():
    id = session.get('userID')
    quanbu = Drink.query.all()
    if request.method == 'GET':
        return render_template('drinkDelete.html', quanbu=quanbu)

    else:
        flag = None
        dID = request.form.get('dID')
        dName=request.form.get('dName')

        ddict={
            'dID':dID,
            'dName':dName
        }
        if dID.strip() is ""and dName.strip() is "":
            #为空
            flag=1
            return render_template('drinkDelete.html', quanbu=quanbu, flag=flag, **ddict)

        if dID.strip() and dName.strip() is "":
            drink = Drink.query.filter(Drink.dID == dID).first()
            if drink:
             db.session.delete(drink)
             db.session.commit()
             flag = 2#成功
             quanbu = Drink.query.all()
             return render_template('drinkDelete.html', quanbu=quanbu, flag=flag, **ddict)

            else:
                flag=3 #找不到匹配的饮品
                return render_template('drinkDelete.html', quanbu=quanbu, flag=flag, **ddict)
        if dID.strip() is "" and dName.strip() :
            drink= Drink.query.filter(Drink.dName == dName).first()
            if drink:
                db.session.delete(drink)
                db.session.commit()
                flag = 2
                quanbu = Drink.query.all()
                return render_template('drinkDelete.html', quanbu=quanbu, flag=flag, **ddict)

            else:
                flag = 3
                return render_template('drinkDelete.html', quanbu=quanbu, flag=flag, **ddict)

        if dID.strip() and dName.strip() :
            drink=Drink.query.filter(and_(Drink.dID == dID,Drink.dName == dName)).first()
            if drink:
                db.session.delete(drink)
                db.session.commit()
                flag = 2
                quanbu = Drink.query.all()
                return render_template('drinkDelete.html', quanbu=quanbu, flag=flag, **ddict)
            else:
                flag = 3
                return render_template('drinkDelete.html', quanbu=quanbu, flag=flag, **ddict)


@blue.route('/recordDelete/', methods=['GET', 'POST'])
def recordDelete():
    id = session.get('userID')
    quanbu = Appointment.query.all()

    if request.method == 'GET':
        return render_template("recordDelete.html", quanbu=quanbu)
    if request.method == 'POST':
        appointmentID = request.form.get('appointmentID')
        ap = Appointment.query.filter(Appointment.appointmentID == appointmentID).first()
        # 删除成功
        if ap:
            db.session.delete(ap)
            db.session.commit()
            book = Book.query.filter(Book.bookID == ap.bookID).first()
            book.bookStorage += ap.bookNum  # 删除记录后归还书籍
            db.session.add(book)
            db.session.commit()
            quanbu = Appointment.query.all()
            flag = 1
            return render_template("recordDelete.html", quanbu=quanbu, flag=flag)
        else:
            # 未找到该记录
            flag = 2
            return render_template("recordDelete.html", quanbu=quanbu, flag=flag)




@blue.route('/cash/', methods=['GET', 'POST'])
def cash():
    id = session.get('userID')
    quanbu = Drink.query.all()
    namelist = []
    for dk in quanbu:
        namelist.append(dk.dName)
    mm = Money.query.filter(Money.ID == 1).first()
    moneyTatal = mm.money

    if request.method == 'GET':
        return render_template('cash.html', quanbu=quanbu,  namelist=namelist,moneyTatal=moneyTatal)
    else:
        buynum=request.form.get('buynum')

        dName = request.form.get('dName')

        if buynum.strip is "":
            flag=1 #购买数量不能为空
            return render_template('cash.html', quanbu=quanbu,  namelist=namelist,flag=flag,moneyTatal=moneyTatal)
        if  dName.strip() is "":
            flag=2 #请输入要购买的饮品
            return render_template('cash.html', quanbu=quanbu, namelist=namelist,flag=flag,moneyTatal=moneyTatal)

        if dName.strip() :  #名有
            dk = Drink.query.filter(Drink.dName ==dName).first()
            if dk:
                if int(buynum)<0 or int(buynum)> dk.dStorage:
                    flag=3#购买饮品数量输入不对，或超出范围
                else:
                    dk.dStorage-=int(buynum)
                    money=int(buynum)*(dk.dSell-dk.dCost)
                    mm=Money.query.filter(Money.ID==1).first()
                    mm.money+=money
                    moneyTatal=mm.money
                    db.session.add(dk)
                    db.session.add(mm)
                    db.session.commit()
                    flag=4
        return render_template('cash.html', quanbu=quanbu, namelist=namelist,flag=4,moneyTatal=moneyTatal)
