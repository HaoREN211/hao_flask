# 作者：hao.ren3
# 时间：2019/11/5 14:34
# IDE：PyCharm

from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}