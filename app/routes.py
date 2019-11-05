# 作者：hao.ren3
# 时间：2019/11/5 14:24
# IDE：PyCharm
from flask import render_template, flash, redirect, url_for
from app import app
from setting import user, title, posts
from app.forms import LoginForm
from config import TranslateLoginForm, TranslatePage

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=title, user=user, posts=posts,
                           home=TranslatePage.Home,
                           login=TranslatePage.Login)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('login'))
    return render_template('login.html',
                           title=title,
                           form=form,
                           login_title=TranslateLoginForm.PageTitle,
                           home=TranslatePage.Home,
                           login=TranslatePage.Login)