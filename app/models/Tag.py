# 作者：hao.ren3
# 时间：2019/11/16 19:53
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import DOUBLE
from datetime import datetime
from app.models.User_action import post_tag

class Tag(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="标签ID")
    tag = db.Column(db.String(20), comment="标签名")
    add_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    posts = db.relationship("Post", secondary=post_tag)

