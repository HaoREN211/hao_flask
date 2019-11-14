# 作者：hao.ren3
# 时间：2019/11/11 15:25
# IDE：PyCharm

from flask import Blueprint
from flask import send_from_directory
from os.path import join

bp = Blueprint('main', __name__)

def favicon():
    return send_from_directory(join(bp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
bp.add_url_rule('/favicon.ico',view_func=favicon)

from app.main.routes import explore, index, user, edit_profile, follow, unfollow, add_post, post, delete_post, edit_post
