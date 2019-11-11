# 作者：hao.ren3
# 时间：2019/11/7 15:42
# IDE：PyCharm
from flask_login import UserMixin
from app import db
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.Post import Post
from datetime import datetime


followers = db.Table('user_followers',
    db.Column('follower_id',
              db.Integer,
              db.ForeignKey('user.id'),
              comment='关注者ID'),
    db.Column('followed_id',
              db.Integer,
              db.ForeignKey('user.id'),
              comment='被关注者ID'),
    db.Column('follow_time',
              db.TIMESTAMP,
              comment='关注时间',
              default=datetime.utcnow()),
    comment='粉丝'
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='用户主键')
    username = db.Column(db.String(64), index=True, unique=True, comment='用户账号名')
    profile_name = db.Column(db.String(64), index=True, comment='用户昵称')
    email = db.Column(db.String(120), index=True, unique=True, comment='用户邮箱地址')
    about_me = db.Column(db.Text, comment='关于我的个人简介')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, comment='用户最后一次登录时间')
    password_hash = db.Column(db.String(128), comment='用户密码')
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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
