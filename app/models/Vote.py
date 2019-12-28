# 作者：hao.ren3
# 时间：2019/12/20 9:40
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime
from operator import and_
from random import choice
from app.models.User import User


class VoteTopic(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='投票主键')
    name = db.Column(db.String(2000), comment="投票主题")
    is_delete = db.Column(db.Boolean, comment="该投票是否被废弃", default=False)
    create_time = db.Column(db.DateTime, comment="创建时间", default=datetime.utcnow())
    create_user = db.Column(BIGINT(unsigned=True), db.ForeignKey('user.id'), index=True, comment='创建者主键')

    options = db.relationship('VoteOption', backref='topic', lazy='dynamic')
    selected = db.relationship('VoteOptionSelected', backref='topic', lazy='dynamic')


    # 获取当前投票的选项列表
    def get_option_names(self):
        list_options = VoteOption.query.filter_by(topic_id=self.id).all()
        option_name = [str(x.name).strip() for x in list_options]
        return option_name

    # 用户今天是否参与了投票
    def is_user_vote_today(self, user_id):
        user_select = VoteOptionSelected.query.filter(
            and_(VoteOptionSelected.user_id == user_id, VoteOptionSelected.topic_id == self.id)).all()
        for current_select in user_select:
            if current_select.create_time.date() == datetime.utcnow().date():
                return True
        return False


    # 统计用户关于该投票主题投票数目
    def user_vote_cnt(self, user_id):
        user_select = VoteOptionSelected.query.filter(
            and_(VoteOptionSelected.user_id == user_id, VoteOptionSelected.topic_id == self.id)).all()
        return len(user_select)


    # 获取date_string那天投过票的人数
    def get_nb_vote_for_a_day(self, date_string):
        user_select = VoteOptionSelected.query.filter_by(
            topic_id=self.id
        ).all()
        list_date = [x.create_time.strftime("%Y-%m-%d") for x in user_select]
        nb_result = 0
        for current_date in list_date:
            if current_date == date_string:
                nb_result += 1
        return nb_result

    # 获取最大最小的投票时间
    def get_max_min_vote_date(self):
        user_select = VoteOptionSelected.query.filter_by(
            topic_id=self.id
        ).all()
        date_format = "%Y-%m-%d"
        min_date = datetime.strptime("2099-01-01", date_format)
        max_date = datetime.strptime("1991-02-11", date_format)
        vote_date = [x.create_time for x in user_select]
        for current_date in vote_date:
            if current_date < min_date:
                min_date = current_date
            if current_date > max_date:
                max_date = current_date
        min_date = datetime.strptime(min_date.strftime(date_format), date_format)
        max_date = datetime.strptime(max_date.strftime(date_format), date_format)
        return max_date, min_date


    # 当前投票的选项按照投票人数从高到底排序
    def get_ordered_options(self):
        list_option = self.options
        list_option = sorted(list_option, key=lambda x:x.nb_user_selected_today(), reverse=True)
        return list_option


    # 随机从选项中选取一个
    def get_today_random_option(self):
        if not self.has_random_option_today():
            self.generate_random_option()
        return self.find_today_random_option()


    # 今天是否有产生过随机选项
    def has_random_option_today(self):
        list_random_option = VoteOptionRandomSelected.query.filter_by(topic_id=self.id).all()
        for current_random_option in list_random_option:
            if current_random_option.create_time.date() == datetime.utcnow().date():
                return True
        return False


    # 获取今天随机产生的选项
    def find_today_random_option(self):
        list_random_option = VoteOptionRandomSelected.query.filter_by(topic_id=self.id).all()
        for current_random_option in list_random_option:
            if current_random_option.create_time.date() == datetime.utcnow().date():
                result_option = current_random_option
                current_option = VoteOption.query.filter_by(id=result_option.option_id).first()
                return current_option.name
        return ""


    # 为今日投票随机选取一个结果
    def generate_random_option(self):
        list_option_id = [x.id for x in self.options]
        current_option_id = choice(list_option_id)
        current_random_option = VoteOptionRandomSelected(
            topic_id=self.id,
            option_id = current_option_id,
        )
        db.session.add(current_random_option)


    def has_voted_users_today(self):
        user_select = VoteOptionSelected.query.filter(VoteOptionSelected.topic_id == self.id).all()
        list_selects, list_users = list([]), list([])
        for current_select in user_select:
            if current_select.create_time.date() == datetime.utcnow().date():
                list_selects.append(current_select)
        for current_select in list_selects:
            list_users.append(User.query.filter_by(id=current_select.user_id).first())
        return list_users

    # 返回投了票的同事名字列表
    def string_names_has_voted_users_today(self):
        result = self.has_voted_users_today()
        result = [x.real_name for x in result]
        return "、".join(result)

    # 返回还没投票的同事名字列表
    def string_names_not_has_voted_users_today(self):
        result = self.has_not_voted_users_today()
        result = [x.real_name for x in result]
        return "、".join(result)

    # 获取今日还没有投票的同事列表
    def has_not_voted_users_today(self):
        list_colleague = User.query.filter_by(is_colleague=1).all()
        list_voted_colleague = self.has_voted_users_today()
        result = list([])
        for current_colleague in list_colleague:
            if not current_colleague in list_voted_colleague:
                result.append(current_colleague)
        return result

    # 统计今日投票了的同事人数
    def nb_voted_users_today(self):
        return len(self.has_voted_users_today())

    # 统计今日还没投票的同事人数
    def nb_not_voted_users_today(self):
        return len(self.has_not_voted_users_today())


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


    # 用户今天是否选择了此选项
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


class VoteOptionRandomSelected(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment='随机结果主键')
    topic_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('vote_topic.id'), comment='投票主题主键')
    option_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('vote_option.id'), comment='投票选项主键')
    create_time = db.Column(db.DateTime, comment="创建时间", default=datetime.utcnow())
