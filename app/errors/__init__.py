# 作者：hao.ren3
# 时间：2019/11/11 14:41
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers