# 作者：hao.ren3
# 时间：2019/11/11 18:05
# IDE：PyCharm

from flask import render_template
from app.main import bp
from flask_login import login_required
from app.model import Post
import markdown

@bp.route('/post/<id>')
@login_required
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    # 分页
    return render_template('post.html', user=post.author, post=post)


