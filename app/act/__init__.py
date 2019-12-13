# 作者：hao.ren3
# 时间：2019/11/12 21:21
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('act', __name__)

from app.act.routes import like, search, comment_post, comment_delete