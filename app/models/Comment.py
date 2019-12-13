# 作者：hao.ren3
# 时间：2019/12/13 11:08
# IDE：PyCharm
from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime

class Comment(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='评论主键')
    post_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('post.id'), nullable=True, comment='评论帖子ID')
    comment_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('comment.id'), nullable=True, comment='评论评论ID')
    comment_user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), comment='评论者ID')
    body = db.Column(db.Text(16777216), comment='评论内容')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='评论创建时间')

    comments = db.relationship(
        'Comment',
        uselist=False,
        remote_side=[id],
        backref=db.backref('comment', uselist=False)
    )
