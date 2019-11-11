# 作者：hao.ren3
# 时间：2019/11/11 15:31
# IDE：PyCharm

from app.main import bp
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.main.forms.edit_post import PostForm
from app.models.Post import  Post
from flask_login import login_required, current_user
from setting import title
from config import TranslatePage, Config
from guess_language import guess_language
from datetime import datetime


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    @login_required的装饰器来拒绝匿名用户的访问以保护某个视图函数。
    :return:
    """
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash('帖子创建成功')
        return redirect(url_for('main.index'))
    # 分页功能
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title=title, form=form,
                           posts=posts.items, home=TranslatePage.Home,
                           login=TranslatePage.Login,
                           next_url=next_url,
                           prev_url=prev_url)
