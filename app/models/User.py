# 作者：hao.ren3
# 时间：2019/11/7 15:42
# IDE：PyCharm
from flask_login import UserMixin
from app import db
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='用户主键')
    username = db.Column(db.String(64), index=True, unique=True, comment='用户账号名')
    profile_name = db.Column(db.String(64), index=True, comment='用户昵称')
    email = db.Column(db.String(120), index=True, unique=True, comment='用户邮箱地址')
    about_me = db.Column(db.Text, comment='关于我的个人简介')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, comment='用户最后一次登录时间')
    password_hash = db.Column(db.String(128), comment='用户密码')
    posts = db.relationship('Post', backref='author', lazy='dynamic')

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
