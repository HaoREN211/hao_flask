# 作者：hao.ren3
# 时间：2019/11/7 17:11
# IDE：PyCharm
from app import app
from flask import render_template
from flask_login import login_required
from setting import user, title, posts
from config import TranslatePage


@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    @login_required的装饰器来拒绝匿名用户的访问以保护某个视图函数。
    :return:
    """
    return render_template("index.html", title=title, posts=posts,
                           home=TranslatePage.Home,
                           login=TranslatePage.Login)