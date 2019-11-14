# 作者：hao.ren3
# 时间：2019/11/12 21:21
# IDE：PyCharm

from flask import Blueprint
from flask import send_from_directory
from os.path import join

bp = Blueprint('act', __name__)

def favicon():
    return send_from_directory(join(bp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
bp.add_url_rule('/favicon.ico',view_func=favicon)

from app.act.routes import like