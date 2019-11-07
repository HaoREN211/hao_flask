# 作者：hao.ren3
# 时间：2019/11/7 17:11
# IDE：PyCharm
from app import app
from flask import render_template
from setting import user, title, posts
from config import TranslatePage

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title=title, user=user, posts=posts,
                           home=TranslatePage.Home,
                           login=TranslatePage.Login)