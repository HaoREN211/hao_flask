# 作者：hao.ren3
# 时间：2019/11/11 16:07
# IDE：PyCharm

from app import db
from app.main import bp
from flask_login import current_user, login_required
from flask import redirect, url_for, flash
from app.model import User


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户{}不存在.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('您不能关注您自己！')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('已关注:{}!'.format(username))
    return redirect(url_for('main.user', username=username))