# 作者：hao.ren3
# 时间：2019/11/12 17:47
# IDE：PyCharm

from app.main import bp
from flask_login import login_required, current_user
from flask import flash, redirect, url_for, render_template, request
from guess_language import guess_language
from app.models.Post import Post
from app.main.forms.add_post import PostForm
from app import db
from app.models.Tag import get_multiple_fields_tags


@bp.route('/edit_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    post_exist = Post.query.filter_by(id=int(post_id)).count()
    if not post_exist:
        flash("帖子不存在")
        return redirect(url_for("main.index"))

    current_post = Post.query.filter_by(id=int(post_id)).first()
    post_author = current_post.author
    if not post_author == current_user:
        flash("您不是帖子的主人，不能对帖子进行修改")
        return redirect(url_for("main.index"))

    form = PostForm()
    if form.validate_on_submit():
        current_post.language = guess_language(form.post.data)
        current_post.body = form.post.data
        current_post.title = form.title.data
        db.session.commit()
        current_post.edit_current_tag(form.list_tags.data)
        flash("帖子修改成功")
        return redirect(url_for("main.post", id=str(post_id)))
    elif request.method == 'GET':
        form.post.data = current_post.body
        form.title.data = current_post.title
        form.list_tags.choices = get_multiple_fields_tags()
        form.list_tags.data = current_post.get_list_tag_id()
    return render_template("add_post.html", form=form, is_edit=True)