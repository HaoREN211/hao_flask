# 作者：hao.ren3
# 时间：2019/11/12 17:02
# IDE：PyCharm

from app.main import bp
from app import db
from flask import request, abort, flash
from flask_login import login_required
from flask import jsonify
from app.models.Post import Post

@bp.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    post_id = request.form['post_id']
    post_exist = Post.query.filter_by(id=int(post_id)).count()

    # 帖子不存在时，报错并退出
    if not post_exist:
        abort(404)
        return jsonify({'result': '帖子'+str(post_id)+'不存在'})

    current_post = Post.query.filter_by(id=int(post_id)).first()
    current_post.remove_all_related_person()
    db.session.delete(current_post)
    db.session.commit()
    flash("帖子删除成功")
    return jsonify({'result': 'success'})