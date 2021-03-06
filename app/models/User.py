# 作者：hao.ren3
# 时间：2019/11/7 15:42
# IDE：PyCharm
from flask_login import UserMixin
from app import db
from sqlalchemy.dialects.mysql import BIGINT
from hashlib import md5
from operator import and_
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.Post import Post
from datetime import datetime, timedelta
from app.models.User_action import user_likes, user_views_user, user_views_post
from permission import Permission


followers = db.Table('user_followers',
    db.Column('follower_id',
              BIGINT(unsigned=True),
              db.ForeignKey('user.id'),
              comment='关注者ID'),
    db.Column('followed_id',
              BIGINT(unsigned=True),
              db.ForeignKey('user.id'),
              comment='被关注者ID'),
    db.Column('follow_time',
              db.TIMESTAMP,
              comment='关注时间',
              default=datetime.utcnow()),
    comment='粉丝'
)


class User(UserMixin, db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='用户主键')
    username = db.Column(db.String(64), index=True, unique=True, comment='用户账号名')
    profile_name = db.Column(db.String(64), index=True, comment='用户昵称')
    email = db.Column(db.String(120), index=True, unique=True, comment='用户邮箱地址')
    about_me = db.Column(db.Text, comment='关于我的个人简介')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, comment='用户最后一次登录时间')
    password_hash = db.Column(db.String(128), comment='用户密码')
    is_colleague = db.Column(db.Boolean, comment="是否是同事", default=False)
    real_name = db.Column(db.String(128), comment='用户真实姓名')
    is_admin = db.Column(db.Boolean, comment='是否是超级管理员', default=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment_author', lazy='dynamic')
    cvs = db.relationship('Cv', backref='author', lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    viewed = db.relationship(
        'User', secondary=user_views_user,
        primaryjoin=(user_views_user.c.viewer_id == id),
        secondaryjoin=(user_views_user.c.viewed_id == id),
        backref=db.backref('viewers', lazy='dynamic'), lazy='dynamic')

    liked_post = db.relationship('Post', secondary = user_likes, lazy='dynamic')
    viewed_post = db.relationship('Post', secondary=user_views_post, lazy='dynamic')
    permissions = db.relationship('Permission', secondary='user_permission', lazy='dynamic')

    # 判断用户是否有编辑简历的权限
    def has_cv_permission(self):
        for current_permission in self.permissions:
            if current_permission.name == Permission.CV:
                return True
        return False

    # 主动评论帖子多少次
    def nb_comments(self):
        return self.comments.count()

    # 帖子被评论多少次
    def nb_commented(self):
        total = 0
        for post in self.posts:
            total += post.nb_comments()
        return total

    # 统计用户总共浏览了多少次帖子
    def sum_views_post(self):
        return self.viewed_post.count()

    # 统计用户的帖子总共被浏览了多少次
    def sum_post_viewed(self):
        nb_viewed = 0
        for post in self.posts:
            nb_viewed += len(post.viewed_user)
        return nb_viewed

    # 统计用户的帖子总共被点赞多少次
    def sum_post_liked(self):
        nb_liked = 0
        for post in self.posts:
            nb_liked += len(post.liked_user)
        return nb_liked

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # 检测该用户十分钟前是否浏览过该用户的主页。
    def check_if_viewed_viewer(self, user):
        compared_time = datetime.utcnow() - timedelta(minutes=10)
        return self.viewed.filter(
            and_(user_views_user.c.viewed_id == user.id,
                 user_views_user.c.view_time >= compared_time)
        ).count() > 0


    # 检测该用户一小时前是否浏览过该用户的主页。
    def check_if_viewed_post(self, post):
        compared_time = datetime.utcnow() - timedelta(hours=1)
        return self.viewed_post.filter(
            and_(user_views_post.c.viewed_id == post.id,
                 user_views_post.c.view_time >= compared_time
                 )).count() > 0


    # 用户浏览帖子
    def view_post(self, post):
        if not self.check_if_viewed_post(post):
            self.viewed_post.append(post)


    # 用户浏览其他用户主页，数据添加浏览数据
    def view_user(self, user):
        if not self.check_if_viewed_viewer(user):
            self.viewed.append(user)


    # 用户主页被浏览次数
    def page_viewed_count(self):
        return self.viewers.count()

    # 用户浏览其他用户主页次数
    def view_user_count(self):
        return self.viewed.count()


    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0


    # 返回当前用户关注对象的最新动态
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def is_liking(self, post):
        return self.liked_post.filter(
            user_likes.c.post_id==post.id
        ).count()>0

    def like(self, post):
        if not self.is_liking(post):
            self.liked_post.append(post)

    def cancel_like(self, post):
        if self.is_liking(post):
            self.liked_post.remove(post)
