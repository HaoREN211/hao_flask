# 作者：hao.ren3
# 时间：2019/11/11 16:48
# IDE：PyCharm

from app.main.forms.edit_post import PostForm
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models.Post import Post
from guess_language import guess_language
from flask import flash, redirect, url_for, render_template


@bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        post = Post(body=form.post.data,
                    body_html=form.post_html.data,
                    author=current_user,
                    language=language,
                    title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash('帖子创建成功')
        return redirect(url_for('main.index'))
    return render_template("add_post.html", form=form)
