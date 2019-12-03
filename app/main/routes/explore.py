# 作者：hao.ren3
# 时间：2019/11/11 15:32
# IDE：PyCharm

from app.main import bp
from flask import render_template, request, url_for
from app.models.Post import Post
from config import Config

@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='发现', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)