# 作者：hao.ren3
# 时间：2019/11/7 15:44
# IDE：PyCharm
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import BIGINT
from app.models.User_action import user_likes, user_views_post, post_tag


class Post(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='帖子主键')
    title = db.Column(db.String(200), comment='帖子标题')
    body = db.Column(db.Text(16777216), comment='帖子内容')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='帖子创建时间')
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), comment='帖子作者的用户ID')
    language = db.Column(db.String(5), comment='语言')

    liked_user = db.relationship('User', secondary=user_likes)
    viewed_user = db.relationship('User', secondary=user_views_post)
    tags = db.relationship('Tag', secondary=post_tag)

    # 判断当前帖子是否被打上标签tag
    def is_post_tagged(self, tag):
        return self.tags.filter(
            post_tag.c.tag_id==tag.id
        ).count()>0

    # 给帖子打上标签
    def add_tag(self, tag):
        if not self.is_post_tagged(tag):
            self.tags.append(tag)

    # 给帖子取消标签
    def remove_tag(self, tag):
        if self.is_post_tagged(tag):
            self.tags.remove(tag)

    # 多少人赞了这条帖子
    def nb_liked_person(self):
        return len(self.liked_user)


    # 删除当前浏览过该帖子的用户
    def remove_viewed_person(self):
        sql = str("DELETE FROM hao_flask.user_views_post WHERE viewed_id=" + str(self.id) + ";")
        db.session.execute(sql)
        db.session.commit()

    # 删除当前给该帖子点赞的用户
    def remove_liked_person(self):
        sql = str("DELETE FROM hao_flask.user_likes WHERE post_id="+str(self.id)+";")
        db.session.execute(sql)
        db.session.commit()

    # 删除当前与该帖子所有有关系的用户
    def remove_all_related_person(self):
        self.remove_viewed_person()
        self.remove_liked_person()
        print("666")

    # 多少人浏览了这条帖子
    def nb_viewed_person(self):
        return len(self.viewed_user)

    def __repr__(self):
        return '<Post {}>'.format(self.body)