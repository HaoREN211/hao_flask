# 作者：hao.ren3
# 时间：2019/11/11 15:25
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main.routes import (explore, index, user, edit_profile, follow, unfollow, add_post, post, delete_post,
                             edit_post, add_tag, tag, service)
