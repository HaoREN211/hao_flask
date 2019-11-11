# 作者：hao.ren3
# 时间：2019/11/11 16:04
# IDE：PyCharm

from app import db
from app.auth import bp
from flask_login import current_user, login_user
from flask import render_template, flash, redirect, url_for
from app.model import User
from app.auth.forms.registration import RegistrationForm


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=True)
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Register', form=form)
