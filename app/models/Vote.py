# 作者：hao.ren3
# 时间：2019/12/20 9:40
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from operator import and_


class VoteTopic(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='投票主键')
    name = db.Column(db.String(2000), comment="投票主题")
    is_delete = db.Column(db.Boolean, comment="该投票是否被废弃", default=False)
    create_time = db.Column(db.DateTime, comment="创建时间", default=datetime.utcnow())
    create_user = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), index=True, comment='创建者主键')

    options = db.relationship('VoteOption', backref='topic', lazy='dynamic')
    selected = db.relationship('VoteOptionSelected', backref='topic', lazy='dynamic')

    # 用户今天是否参与了投票
    def is_user_vote_today(self, user_id):
        user_select = VoteOptionSelected.query.filter(
            and_(VoteOptionSelected.user_id == user_id, VoteOptionSelected.topic_id == self.id)).all()
        for current_select in user_select:
            if current_select.create_time.date() == datetime.utcnow().date():
                return True
        return False

class VoteOption(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='投票选项主键')
    topic_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('vote_topic.id'), comment='投票主题主键')
    name = db.Column(db.String(2000), comment="投票选项")
    is_delete = db.Column(db.Boolean, comment="该投票是否被废弃", default=False)
    create_time = db.Column(db.DateTime, comment="创建时间", default=datetime.utcnow())
    create_user = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), index=True, comment='创建者主键')

    selected = db.relationship('VoteOptionSelected', backref='option', lazy='dynamic')


    # 新增用户投票
    def user_vote(self, user_id):
        new_option_selected = VoteOptionSelected(
            topic_id=self.topic_id,
            option_id=self.id,
            user_id=user_id
        )
        db.session.add(new_option_selected)
        db.session.commit()


    def is_user_selected_today(self, user_id):
        user_select = VoteOptionSelected.query.filter(
            and_(VoteOptionSelected.user_id==user_id, VoteOptionSelected.option_id==self.id)).all()
        for current_select in user_select:
            if current_select.create_time.date() == datetime.utcnow().date():
                return True
        return False

    # 该选项今天被选了多少次
    def nb_user_selected_today(self):
        user_select = VoteOptionSelected.query.filter( VoteOptionSelected.option_id==self.id).all()
        result = 0
        for current_select in user_select:
            if current_select.create_time.date() == datetime.utcnow().date():
                result += 1
        return result


class VoteOptionSelected(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='用户投票结果主键')
    topic_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('vote_topic.id'), comment='投票主题主键')
    option_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('vote_option.id'), comment='投票选项主键')
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), index=True, comment='创建者主键')
    create_time = db.Column(db.DateTime, comment="创建时间", default=datetime.utcnow())




