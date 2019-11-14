# 作者：hao.ren3
# 时间：2019/11/7 15:44
# IDE：PyCharm
from datetime import datetime
from app import db
from app.models.User_action import user_likes, user_views_post


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='帖子主键')
    title = db.Column(db.String(200), comment='帖子标题')
    body = db.Column(db.Text(16777216), comment='帖子内容')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='帖子创建时间')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='帖子作者的用户ID')
    language = db.Column(db.String(5), comment='语言')

    liked_user = db.relationship('User', secondary=user_likes)
    viewed_user = db.relationship('User', secondary=user_views_post)

    # 多少人赞了这条帖子
    def nb_liked_person(self):
        return len(self.liked_user)

    # 多少人浏览了这条帖子
    def nb_viewed_person(self):
        return len(self.viewed_user)

    def __repr__(self):
        return '<Post {}>'.format(self.body)