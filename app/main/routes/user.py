# 作者：hao.ren3
# 时间：2019/11/11 15:50
# IDE：PyCharm

from flask import render_template, request, url_for, g
from app.main import bp
from flask_login import login_required, current_user
from app.models.Post import Post
from app.model import User
from config import Config

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    # 添加用户浏览事件
    if not user == current_user:
        if not current_user.is_anonymous:
            current_user.view_user(user)

    # 分页
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
