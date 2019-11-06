# 作者：hao.ren3
# 时间：2019/11/5 16:35
# IDE：PyCharm

import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-hao-guess'
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'hhaixdw'
    HOST = 'localhost'
    PORT = '3306'
    DATABASE = 'hao_flask'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 5


class TranslateLoginForm(object):
    Username = "账号"
    Password = "密码"
    PageTitle = "请登录"
    RememberMe = "请记住我"
    submit = "登录"

class TranslatePage(object):
    Home = "主页"
    Login = "登录"