#author:gexianmeng
from flask import Flask, session
from flask_script import Manager

from back.models import db
from back.views import back_blueprint
from web.views import web_blueprint

app = Flask(__name__)
app.register_blueprint(blueprint=back_blueprint,url_prefix='/back')
app.register_blueprint(blueprint=web_blueprint,url_prefix='/web')
app.secret_key = 'dqhwdhqiqwidhiqhd'

#配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:654g-n89s-hyt3@127.0.0.1:3306/blog'
db.init_app(app)


if __name__ == '__main__':
    manage = Manager(app)
    manage.run()
