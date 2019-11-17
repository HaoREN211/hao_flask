# 作者：hao.ren3
# 时间：2019/11/17 19:45
# IDE：PyCharm

from app.main import bp
from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main.forms.add_tags import TagForm
from app.models.Tag import Tag, get_all_tag_name
from app import db
from datetime import datetime


@bp.route('/add_tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    form = TagForm()
    all_tags = get_all_tag_name()
    if form.validate_on_submit():
        tag = Tag(
            tag=form.tag.data,
            add_user=current_user.id,
            add_time=datetime.utcnow()
        )
        db.session.add(tag)
        db.session.commit()
        flash("标签创建成功")
        return redirect(url_for('main.add_tag'))
    return render_template("add_tag.html", form=form, tags=all_tags)