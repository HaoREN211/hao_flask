# 作者：hao.ren3
# 时间：2019/11/5 16:35
# IDE：PyCharm

import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-hao-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql:///localhost'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TranslateLoginForm(object):
    Username = "账号"
    Password = "密码"
    PageTitle = "请登录"
    RememberMe = "请记住我"
    submit = "登录"

class TranslatePage(object):
    Home = "主页"
    Login = "登录"