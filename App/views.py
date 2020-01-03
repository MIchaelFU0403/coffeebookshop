from flask import *
from App.models import Client
from App.models1 import Drink,Money
from App.models2 import Book,Appointment
from sqlalchemy import and_
from App.ext import db

blue = Blueprint('blue',__name__)

def init_blue(app):
    app.register_blueprint(blueprint=blue)

@blue.route('/')
def index():
     db.create_all()
     return render_template("FlexAlbum.html")

@blue.route('/register/', methods=['GET', 'POST'])
def register():
    flag=None
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        userage = request.form.get('userage')
        userID = request.form.get('userID')
        userPhone = request.form.get('userPhone')
        email = request.form.get('email')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        gender = request.form.get('gender')
        position = request.form.get('position')
        userdict = {
            'username': username,
            'userage': userage,
            'userID': userID,
            'userPhone': userPhone,
            'userEmail': email,
            'userPassword1': pwd1,
            'userPassword2':pwd2,
            'userSex': gender,
            'userPosition': position
        }
        user = Client.query.filter(Client.userID == userID).first()
        if user:
            flag=1
            # flash(u'ID被注册过了')
            return render_template("register.html",flag=flag,**userdict)

        user=Client.query.filter(Client.userPhone == userPhone).first()
        if user:
            flag=2
            # flash(u'手机号被注册过了')
            return render_template("register.html",flag=flag,**userdict)
        user = Client.query.filter(Client.userEmail == email).first()
        if user:
            flag=3
            # flash(u'电子邮箱被注册过了')
            return render_template("register.html",flag=flag,**userdict)
        if all([username, userage, userID,userPhone,email,pwd1,pwd2,gender,position]):
            if pwd1 == pwd2:
                if (len(userPhone)== 11 ):
                    a = Client()
                    a.userID=userID
                    a.userPhone=userPhone
                    a.userEmail=email
                    a.userName = username
                    a.userAge = userage
                    a.userSex = gender
                    a.userPosition = position
                    a.userPassword = pwd1
                    db.session.add(a)
                    db.session.commit()
                   # flash('注册成功')
                    return redirect(url_for('blue.login'))

                else:
                    flag=4
                    # flash(u' 手机号长度不为11位')
                    return render_template("register.html",flag=flag,**userdict)

            else:
                flag=5
                #flash('两次密码输入不一致')
                return render_template("register.html",flag=flag,**userdict)

         # flash('输入信息不全')前端实现了
         # request 从请求里读内容
    return render_template("register.html",flag=flag,**userdict)

@blue.route('/login/', methods=['GET', 'POST'])
def login():
        message=None
        if request.method == 'GET':
            return render_template('login.html')
        else:
            username = request.form.get('username')
            userID= request.form.get('userID')
            userpwd = request.form.get('userpwd')
            if all ([username,userID,userpwd]):
                user=Client.query.filter(Client.userID==userID,Client.userName==username,Client.userPassword==userpwd).first()
                if user and user.userPosition=='A':
                    session['userID'] = user.userID
                    session.permanent = True
                    # print(session.get('userID'))
                    # flash(u"登陆成功",'success')
                    return redirect(url_for('blue.mainPage'))
                if user and user.userPosition=='U':
                    session['userID'] = user.userID
                    session.permanent = True
                    # print(session.get('userID'))
                    # flash(u"登陆成功",'success')
                    return redirect(url_for('blue.clientMainPage'))


                else:
                    flash( u'用户名,或学号或者密码错误！')
                    return redirect(url_for('blue.login'))
            else:
                flash( u'用户名,或学号或者密码填写不完整！')
                return render_template('login.html')



@blue.route('/logout/')
def logout():
     session.clear()
     return redirect(url_for('blue.index'))


@blue.route('/ReverseCard/')
def ReverseCard():
    return render_template("ReverseCard.html")

@blue.route('/web_design/')
def web_design():
    return render_template("PersionWebsite.html")

@blue.route('/Loading/')
def Loading():
    return render_template("Loading.html")

@blue.route('/aboutus/')
def aboutus():
    return render_template("aboutus.html")




@blue.route('/mainPage/')
def mainPage():
    id=session.get('userID')
    user = Client.query.filter(Client.userID == id).first()
    userdict={
            'username':user.userName,
            'userage': user.userAge,
            'userID' :user.userID,
            'userPhone': user.userPhone,
            'userEmail':  user.userEmail,
            'userPassword':  user.userPassword,
             'userSex' :user.userSex,
            'userPosition':  user.userPosition
            }
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    paginate = Appointment.query.paginate(page, per_page, error_out=False)
    quanbu = paginate.items
    return render_template("mainPage.html", paginate=paginate, quanbu=quanbu, **userdict)

@blue.route('/notice/')
def notice():
    return render_template("LayeredImage.html")



@blue.route('/clientMainPage/')
def clientMainPage():
    id=session.get('userID')
    user = Client.query.filter(Client.userID == id).first()

    userdict={
            'username':user.userName,
            'userage': user.userAge,
            'userID' :user.userID,
            'userPhone': user.userPhone,
            'userEmail':  user.userEmail,
            'userPassword':  user.userPassword,
             'userSex' :user.userSex,
            'userPosition':  user.userPosition
            }
    return render_template("clientMainPage.html",**userdict)




