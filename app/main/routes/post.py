# 作者：hao.ren3
# 时间：2019/11/11 18:05
# IDE：PyCharm

from flask import render_template
from app.main import bp
from app.model import Post


@bp.route('/post/<id>')
def post(id):
    inside_post = Post.query.filter_by(id=id).first_or_404()
    # 分页
    return render_template('post.html', user=inside_post.author, post=inside_post)


