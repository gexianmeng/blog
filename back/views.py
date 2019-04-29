#author:gexianmeng
from flask import Blueprint,render_template,request,\
    redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash

from back.models import db,Article,ArticleType,User
from utils.functions import is_login

back_blueprint = Blueprint('back',__name__)


@back_blueprint.route('/index/',methods=['GET'])
def index():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    username = user.username
    count = len(User.query.all())
    article_count = len(Article.query.all())
    return render_template('back/index.html',username=username,count=count,
                           article_count=article_count)


@back_blueprint.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账号已注册，请更换账号'
                return render_template('back/register.html',error=error)
            else:
                if password2 == password:
                    user = User()
                    user.username = username
                    user.password =generate_password_hash(password)
                    user.save()
                    return redirect(url_for('back.login'))
                else:
                    error = '两次密码不一致'
                    return render_template('back/register.html',error=error)
        else:
            error = '请填写完整的信息'
            return render_template('back/register.html',error=error)


@back_blueprint.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在，请注册'
                return render_template('back/register.html',error=error)
            if not check_password_hash(user.password,password):
                error = '密码错误，请重新输入密码'
                return render_template('back/login.html',error=error)

            session['user_id'] = user.id
            return redirect(url_for('back.index'))
        else:
            error = '请填写完整的登录信息'
            print(3)
            return render_template('back/login.html',error=error)


@back_blueprint.route('/Logout/',methods=['GET'])
def Logout():
    del session['user_id']
    return redirect(url_for('back.login'))


@back_blueprint.route('/a_type/',methods=['GET','POST'])
def a_type():
    # if request.method == 'GET':
    types = ArticleType.query.all()
    request.form.get('fid')
    return render_template('back/category.html',types=types)


@back_blueprint.route('/add_type/',methods=['GET','POST'])
def add_type():
    if request.method == 'GET':
        return render_template('back/categroy.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            art_type = ArticleType()
            art_type.t_name = atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.a_type'))
        else:
            error = '请填写分类信息'
            return render_template('back/categroy.html',error=error)


@back_blueprint.route('/del_type/<int:id>',methods=['GET','POST'])
def del_type(id):
    #删除分类
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


@back_blueprint.route('/update_type/<int:id>',methods=['GET','POST'])
def update_type(id):
    if request.method =='GET':
        return render_template('back/update_category.html')
    if request.method == 'POST':
        type1 = ArticleType.query.get(id)
        rename = request.form.get('name')
        type1.t_name = rename
        db.session.add(type1)
        db.session.commit()
        return redirect(url_for('back.a_type'))


@back_blueprint.route('/article/',methods=['GET','POST'])
def article():
    articles = Article.query.all()
    return render_template('back/article.html',articles=articles)


@back_blueprint.route('/add_article/',methods=['GET','POST'])
def add_article():
    if request.method == 'GET':
        types=ArticleType.query.all()
        return render_template('back/add-article.html',types=types)
    if request.method == 'POST':
        title = request.form.get('title')
        type = request.form.get('category')
        desc = request.form.get('describe')
        content = request.form.get('content')


        if title and desc and content and type:
            article = Article()
            article.title = title
            article.desc = desc
            article.type = type
            article.content = content
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('back.article'))
        else:
            error = '请填写完整的文章信息'
            return render_template('back/article.html',error=error)


@back_blueprint.route('/delete_article/<int:id>',methods=['GET'])
def delete_article(id):

    article = Article.query.get(id)
    print(article)
    db.session.delete(article)
    db.session.commit()
    return render_template('back/article.html')


@back_blueprint.route('/update_article/<int:id>',methods=['GET','POST'])
def update_article(id):

    if request.method == 'GET':
        types=ArticleType.query.all()
        article = Article.query.filter(Article.id==id).first()
        return render_template('back/update_article.html',article=article,types=types)

    if request.method == 'POST':

        retitle = request.form.get('title')
        retype = request.form.get('category')
        redesc = request.form.get('describe')
        recontent = request.form.get('content')
        article = Article.query.filter(Article.id == id).first()
        article.title = retitle
        article.desc = redesc
        article.type = retype
        article.content = recontent
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('back.article'))


