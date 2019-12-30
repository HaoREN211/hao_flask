# 作者：hao.ren3
# 时间：2019/11/12 21:03
# IDE：PyCharm
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import BIGINT


user_likes = db.Table('user_likes',
    db.Column('user_id',
        BIGINT(unsigned=True),
        db.ForeignKey('user.id'),
        comment='点赞者ID'),
    db.Column('post_id',
        BIGINT(unsigned=True),
        db.ForeignKey('post.id'),
        comment='被点赞帖子'),
    db.Column('likes_time',
          db.TIMESTAMP,
          comment='点赞时间',
          default=datetime.utcnow()),
)


user_views_user = db.Table('user_views_user',
    db.Column('viewer_id',
        BIGINT(unsigned=True),
        db.ForeignKey('user.id'),
        comment='浏览者ID'),
    db.Column('viewed_id',
        BIGINT(unsigned=True),
        db.ForeignKey('user.id'),
        comment='被浏览者ID'),
    db.Column('view_time',
          db.TIMESTAMP,
          comment='浏览时间',
          default=datetime.utcnow()),
    comment='用户浏览用户事件'
)


user_views_post = db.Table('user_views_post',
    db.Column('viewer_id',
        BIGINT(unsigned=True),
        db.ForeignKey('user.id'),
        comment='浏览者ID'),
    db.Column('viewed_id',
        BIGINT(unsigned=True),
        db.ForeignKey('post.id'),
        comment='被浏览帖子ID'),
    db.Column('view_time',
          db.TIMESTAMP,
          comment='浏览时间',
          default=datetime.utcnow()),
    comment='用户浏览帖子事件'
)


post_tag = db.Table(
    'post_tag',
    db.Column('post_id',
        BIGINT(unsigned=True),
        db.ForeignKey('post.id'),
        comment='帖子ID'),
    db.Column('tag_id',
        BIGINT(unsigned=True),
        db.ForeignKey('tag.id'),
        comment='标签ID'),
    db.Column('view_time',
          db.TIMESTAMP,
          comment='标签添加时间',
          default=datetime.utcnow()),
    comment='用户添加帖子标签'
)

user_permission = db.Table('user_permission',
    db.Column('id',
        BIGINT(unsigned=True),
        primary_key=True,
        comment='用户权限ID'),
    db.Column('permission_id',
        BIGINT(unsigned=True),
        db.ForeignKey('permission.id'),
        comment='权限ID'),
    db.Column('user_id',
        BIGINT(unsigned=True),
        db.ForeignKey('user.id'),
        comment='用户ID'),
    db.Column('create_time',
          db.TIMESTAMP,
          comment='创建时间',
          default=datetime.utcnow()),
)