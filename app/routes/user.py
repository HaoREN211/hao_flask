# 作者：hao.ren3
# 时间：2019/11/7 17:15
# IDE：PyCharm

from flask import render_template
from app import app
from flask_login import login_required, current_user
from app import db
from app.model import User
from datetime import datetime


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    # posts = user.posts
    return render_template('user.html', user=user, posts=posts)


# 记录用户的最后访问时间
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
