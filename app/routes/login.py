# 作者：hao.ren3
# 时间：2019/11/7 16:57
# IDE：PyCharm
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from config import TranslatePage
from flask import redirect, url_for, flash, render_template
from app.model import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template("login.html", title='Sign In', form=form,
                           home=TranslatePage.Home,
                           login=TranslatePage.Login)