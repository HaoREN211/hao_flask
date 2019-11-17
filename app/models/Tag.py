# 作者：hao.ren3
# 时间：2019/11/16 19:53
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from app.models.User_action import post_tag


# 获取数据库中所有tag的列表，并将格式转化成为multiple_field能接受的格式
def get_multiple_fields_tags():
    tags = Tag.query.all()
    list_tags = list([])
    for tag in tags:
        list_tags.append((tag.id, str(tag.tag)))
    return list_tags


# 获取当前所有的tag名称
def get_all_tag_name():
    tags = Tag.query.all()
    list_tags = list([])
    for tag in tags:
        list_tags.append(str(tag.tag))
    return list_tags


class Tag(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="标签ID")
    tag = db.Column(db.String(20), comment="标签名", unique=True)
    add_user = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), comment="创建用户")
    add_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    posts = db.relationship("Post", secondary=post_tag)

