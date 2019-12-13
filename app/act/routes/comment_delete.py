# 作者：hao.ren3
# 时间：2019/12/13 14:00
# IDE：PyCharm
from app import db
from app.act import bp
from flask_login import login_required
from app.models.Comment import Comment
from flask import flash, redirect, url_for


@bp.route("/comment_delete/<post_id>/<id>", methods=['GET'])
@login_required
def comment_delete(post_id, id):
    current_comment = Comment.query.filter_by(id=id).all()
    nb_result = len(current_comment)
    if nb_result == 0:
        flash("评论不存在，不能进行删除")
    else:
        current_comment = current_comment[0]
        db.session.delete(current_comment)
        db.session.commit()
        flash("评论删除成功")
    return redirect("/post/"+str(post_id)+"#blog_comment")