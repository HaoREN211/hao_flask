# 作者：hao.ren3
# 时间：2019/11/7 17:15
# IDE：PyCharm

from flask import render_template
from app import app
from flask_login import login_required
from app.model import User


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)