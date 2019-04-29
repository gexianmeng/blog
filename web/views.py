#author:gexianmeng
from flask import Blueprint,render_template,request,\
    redirect,url_for,session

from back.models import db,Article,ArticleType,User
from utils.functions import is_login

web_blueprint = Blueprint('web',__name__)

@web_blueprint.route('/index/',methods=['GET'])
def index():
    types = ArticleType.query.all()
    articles = Article.query.all()
    # article_type = ArticleType.query.filter(ArticleType.id==id).first()
    # t_name = article_type.t_name

    return render_template('web/index.html',articles=articles,types=types)


@web_blueprint.route('/share/',methods=['GET'])
def share():
    return render_template('web/share.html')


@web_blueprint.route('/about/',methods=['GET'])
def about():
    articles = Article.query.all()
    types = ArticleType.query.all()
    # for type in types:
    #     length = len(type)
    #     print(length)
    return render_template('web/about.html',types=types,articles=articles)


@web_blueprint.route('/show/<int:id>',methods=['GET'])
def show(id):
    article = Article.query.filter(Article.id==id).first()
    return render_template('web/show.html',article=article)