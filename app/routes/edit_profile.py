# @Time    : 2019/11/10 20:03
# @Author  : REN Hao
# @FileName: edit_profile.py
# @Software: PyCharm

from app.forms import EditProfileForm
from flask_login import login_required, current_user
from flask import flash, redirect, url_for, request, render_template
from app import app, db
from config import ChineseLanguage


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(ChineseLanguage.Profile.saved)
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           title=ChineseLanguage.Profile.edit_profile,
                           form=form)
