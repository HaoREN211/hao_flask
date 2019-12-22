# 作者：hao.ren3
# 时间：2019/12/22 9:42
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('data', __name__)

from app.data.routes import vote