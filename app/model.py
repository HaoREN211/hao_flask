# @Time    : 2019/11/5 22:35
# @Author  : REN Hao
# @FileName: model.py
# @Software: PyCharm

from app import login
from app.models.User import User
from app.models.Post import Post
from app.models.Tag import Tag

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
