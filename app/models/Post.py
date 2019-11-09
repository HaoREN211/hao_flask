# 作者：hao.ren3
# 时间：2019/11/7 15:44
# IDE：PyCharm
from datetime import datetime
from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='帖子主键')
    body = db.Column(db.Text(16777216), comment='帖子内容')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='帖子创建时间')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='帖子作者的用户ID')

    def __repr__(self):
        return '<Post {}>'.format(self.body)