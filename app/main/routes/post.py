# 作者：hao.ren3
# 时间：2019/11/11 18:05
# IDE：PyCharm

from flask import render_template, request
from flask_login import current_user
from app.main import bp
from app.model import Post


@bp.route('/post/<id>')
def post(id):
    inside_post = Post.query.filter_by(id=id).first_or_404()

    if (request.method=='GET') and (not current_user.is_anonymous):
        if not inside_post.author == current_user:
            current_user.view_post(inside_post)
    tags = inside_post.get_all_tags_name()
    # 分页
    return render_template('post.html', user=inside_post.author, post=inside_post, tags=tags, title=inside_post.title)


