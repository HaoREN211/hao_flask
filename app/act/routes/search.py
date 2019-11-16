# 作者：hao.ren3
# 时间：2019/11/16 14:16
# IDE：PyCharm

from app.act import bp
from flask_login import login_required
from flask import url_for, render_template, request
from app.models.Post import Post
from config import Config
from operator import or_

@bp.route("/search/<search_content>", methods=['GET', 'POST'])
@login_required
def search(search_content):
    posts = Post.query.filter(
        or_(Post.body.like("%"+str(search_content)+"%"),
            Post.title.like("%" + str(search_content) + "%")
            ))
    page = request.args.get('page', 1, type=int)
    posts = posts.paginate(
        page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html",
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)