# 作者：hao.ren3
# 时间：2019/11/12 21:25
# IDE：PyCharm

from app.act import bp
from flask_login import login_required, current_user
from flask import redirect, url_for, flash
from app.models.Post import Post

@bp.route("/like/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    current_user.like(post)
    flash("点赞成功")
    return redirect(url_for("main.post", id=post_id))


@bp.route("/cancel_like/<post_id>", methods=['GET'])
@login_required
def cancel_like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    current_user.cancel_like(post)
    flash("取消点赞")
    return redirect(url_for("main.post", id=post_id))


