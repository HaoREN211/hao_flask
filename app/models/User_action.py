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


user_views_user = db.Table('user_views_user',
    db.Column('viewer_id',
        db.Integer,
        db.ForeignKey('user.id'),
        comment='浏览者ID'),
    db.Column('viewed_id',
        db.Integer,
        db.ForeignKey('user.id'),
        comment='被浏览者ID'),
    db.Column('view_time',
          db.TIMESTAMP,
          comment='浏览时间',
          default=datetime.utcnow()),
    comment='用户浏览用户事件'
)