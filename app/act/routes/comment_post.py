# 作者：hao.ren3
# 时间：2019/12/13 10:54
# IDE：PyCharm

from app.act import bp
from app import db
from flask import request, flash, redirect, url_for
from flask_login import login_required
from app.models.Comment import Comment

@bp.route("/comment_post", methods=['POST'])
@login_required
def comment_post():
    comment_user_id = request.form["comment_user_id"]
    post_id = request.form["post_id"]
    comment_body = request.form["comment_body"]

    current_comment = Comment(
        post_id = post_id,
        comment_user_id = comment_user_id,
        body = comment_body
    )
    db.session.add(current_comment)
    db.session.commit()

    flash("评论创建成功")
    return redirect("/post/"+str(post_id)+"#blog_comment")

