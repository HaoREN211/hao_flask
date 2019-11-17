# 作者：hao.ren3
# 时间：2019/11/11 16:48
# IDE：PyCharm

from app.main.forms.add_post import PostForm
from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.models.Post import Post
from app.models.Tag import Tag
from guess_language import guess_language
from flask import flash, redirect, url_for, render_template
from datetime import datetime
from operator import and_


@bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        print(form.list_tags.data)
        now = datetime.utcnow()
        post = Post(body=form.post.data,
                    author=current_user,
                    language=language,
                    timestamp=now,
                    title=form.title.data)
        db.session.add(post)
        db.session.commit()
        add_tags_for_new_post(current_user.id, now, form.list_tags.data)
        flash('帖子创建成功')
        return redirect(url_for('main.index'))
    return render_template("add_post.html", form=form)


# 给新加的post打上标签
def add_tags_for_new_post(author_id, created_time, list_tags):
    post = Post.query.filter(and_(Post.user_id==author_id, Post.timestamp==created_time)).first()
    for tag_id in list_tags:
        tag = Tag.query.filter_by(id=int(tag_id)).first()
        post.add_tag(tag)
