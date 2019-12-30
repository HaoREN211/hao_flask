# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/29 9:32
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime

class Permission(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="权限主键")
    name = db.Column(db.String(20), nullable=False, comment="权限说明")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")

