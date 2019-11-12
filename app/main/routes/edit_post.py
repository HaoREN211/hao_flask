# 作者：hao.ren3
# 时间：2019/11/12 17:47
# IDE：PyCharm

from app.main import bp
from flask_login import login_required, current_user
from flask import flash, redirect, url_for, render_template
from guess_language import guess_language
from app.models.Post import Post
from app.main.forms.add_post import PostForm
from app import db


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

    # 先将post表单里的数据保存在临时变量里
    # 不然提交了表单之后，会将数据库原来的数据重新赋值给已经编辑过的数据
    temp_post_data = form.post.data
    temp_post_title = form.title.data
    form.post.data = current_post.body
    form.title.data = current_post.title

    if form.validate_on_submit():
        current_post.language = guess_language(temp_post_data)
        current_post.body = temp_post_data
        current_post.title = temp_post_title
        db.session.commit()
        flash("帖子修改成功")
        return redirect(url_for("main.post", id=str(post_id)))

    return render_template("add_post.html", form=form, is_edit=True)