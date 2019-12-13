# 作者：hao.ren3
# 时间：2019/12/3 15:19
# IDE：PyCharm

from flask import render_template, request, url_for
from app.main import bp
from app.models.Post import Post
from app.models.Tag import Tag
from config import Config

@bp.route('/tag/<tag_name>')
def tag(tag_name):
    current_tag = Tag.query.filter_by(tag=tag_name).first()
    posts = current_tag.posts

    # 手动分页
    nb_post_per_page = Config.POSTS_PER_PAGE
    page = request.args.get('page', 1, type=int)

    # 计算当前页面的第一个post和最后一个post的索引
    start_index = (page-1)*nb_post_per_page
    end_index = nb_post_per_page*page


    has_prev = True
    has_next = True
    next_num = page + 1
    prev_num = page - 1

    if page == 1:
        has_prev = False
    if end_index>=len(posts)-1:
        has_next = False

    posts = posts[start_index:end_index]

    next_url = url_for('main.explore', page=next_num) \
        if has_next else None
    prev_url = url_for('main.explore', page=prev_num) \
        if has_prev else None

    return render_template('index.html', title='标签:'+tag_name, posts=posts,
                           next_url=next_url,
                           prev_url=prev_url,
                           tag_name=tag_name)