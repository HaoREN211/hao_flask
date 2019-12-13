# 作者：hao.ren3
# 时间：2019/11/7 15:44
# IDE：PyCharm
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import BIGINT
from app.models.User_action import user_likes, user_views_post, post_tag
from app.models.Tag import Tag


class Post(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='帖子主键')
    title = db.Column(db.String(200), comment='帖子标题')
    body = db.Column(db.Text(16777216), comment='帖子内容')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, comment='帖子创建时间')
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), comment='帖子作者的用户ID')
    language = db.Column(db.String(5), comment='语言')

    liked_user = db.relationship('User', secondary=user_likes)
    viewed_user = db.relationship('User', secondary=user_views_post)
    tags = db.relationship('Tag', secondary=post_tag, lazy='dynamic')
    comments = db.relationship('Comment', backref='post_comment', lazy='dynamic')

    # 判断当前帖子是否被打上标签tag
    def is_post_tagged(self, tag):
        return self.tags.filter(
            post_tag.c.tag_id==tag.id
        ).count()>0

    # 获取当前帖子被打上的标签的id列表
    def get_list_tag_id(self):
        list_tags = list([])
        for tag in self.tags:
            list_tags.append(str(tag.id))
        return list_tags

    # 修改编辑后的帖子标签
    def edit_current_tag(self, list_tag_id):
        self.add_tag_in_list(list_tag_id)
        self.remove_tag_not_in_list(list_tag_id)

    # 获取当前帖子被打上标签的所有标签名
    def get_all_tags_name(self):
        list_result = list([])
        for current_tag in self.tags:
            list_result.append(current_tag.tag)
        return list_result

    # 帖子新增的标签
    # 也就是新增前端传回来的list_tag_id中数据库没有的tag_id
    def add_tag_in_list(self, list_tag_id):
        for current_tag_id in list_tag_id:
            current_tag = Tag.query.filter_by(id=int(current_tag_id)).first()
            self.add_tag(current_tag)

    # 帖子被删除掉的标签
    def remove_tag_not_in_list(self, list_tag_id):
        list_id = []
        for current_tag in self.tags:
            list_id.append(str(current_tag.id))
        delete_tags_id = list(set(list_id) - set(list_tag_id))
        for current_tag_id in delete_tags_id:
            current_tag = Tag.query.filter_by(id=int(current_tag_id)).first()
            self.remove_tag(current_tag)

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

    # 多少人评论了此帖子
    def nb_comments(self):
        return self.comments.count()

    def __repr__(self):
        return '<Post {}>'.format(self.body)