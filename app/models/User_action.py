# 作者：hao.ren3
# 时间：2019/11/12 21:03
# IDE：PyCharm
from datetime import datetime
from app import db

user_likes = db.Table('user_likes',
    db.Column('user_id',
        db.Integer,
        db.ForeignKey('user.id'),
        comment='点赞者ID'),
    db.Column('post_id',
        db.Integer,
        db.ForeignKey('post.id'),
        comment='被点赞帖子'),
    db.Column('likes_time',
          db.TIMESTAMP,
          comment='点赞时间',
          default=datetime.utcnow()),
)