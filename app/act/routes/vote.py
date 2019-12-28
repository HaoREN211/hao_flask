# 作者：hao.ren3
# 时间：2019/12/20 9:36
# IDE：PyCharm

from app.act import bp
from app import db
from flask_login import login_required
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.models.Vote import VoteTopic, VoteOption, VoteOptionSelected
from operator import and_
import datetime
from math import floor
from app.act.forms.echarts_form import VoteLineChartData, VoteRadarData
from app.models.User import User
from app.act.forms.vote import VoteOptionAddForm


# 折线图数据，每日投票情况
def vote_line_chart_data(id):
    current_topic = VoteTopic.query.filter_by(id=id).first()
    max_date, min_date = current_topic.get_max_min_vote_date()

    list_date, list_data = list([]), list([])
    nb_date = (max_date - min_date).days + 1

    max_cnt = 0
    min_cnt = 9999
    interval = 5

    for current_index in range(nb_date):
        current_date = (min_date + datetime.timedelta(days=current_index)).strftime("%Y-%m-%d")
        nb_vote = current_topic.get_nb_vote_for_a_day(current_date)

        if nb_vote > max_cnt:
            max_cnt = nb_vote
        if nb_vote < min_cnt:
            min_cnt = nb_vote

        # 计算y轴刻度间距
        if (max_cnt - min_cnt) < 5:
            interval = 1
        else:
            interval = floor(float(max_cnt - min_cnt) / float(5))

        list_data.append(nb_vote)
        list_date.append(current_date)
    return VoteLineChartData(
        vote_cnt=list_data,
        vote_date=list_date,
        max_cnt=max_cnt,
        min_cnt=min_cnt,
        interval=interval
    )


# 雷达图，每人投票情况
def vote_radar_data(id):
    current_topic = VoteTopic.query.filter_by(id=id).first()
    list_colleague = User.query.filter_by(is_colleague=1).all()
    list_name, list_nb_vote, list_names_string = list([]), list([]), list([])
    nb_vote = 0

    for current_colleague in list_colleague:
        if (current_colleague.real_name is not None) and (current_colleague.real_name != ""):
            list_nb_vote.append(current_topic.user_vote_cnt(current_colleague.id))
            list_name.append(current_colleague.real_name)
            nb_vote += 1

    if nb_vote > 0:
        max_cnt = max(list_nb_vote)
        min_cnt = min(list_nb_vote)
        list_names_string = ['{"name":"' + list_name[x] + '", "max": ' + str(max_cnt) + ', "min": ' + str(min_cnt) + '}' for x
                             in range(nb_vote)]
        return VoteRadarData(
            list_name=list_names_string, data=list_nb_vote
        )
    return VoteRadarData(
        list_name=[""],
        data=[0]
    )


@bp.route("/vote/<vote_id>", methods=['GET', 'POST'])
@login_required
def vote(vote_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()

    if not current_vote.has_random_option_today():
        current_vote.generate_random_option()

    random_option = current_vote.find_today_random_option()

    data_vote_line_chart = vote_line_chart_data(vote_id)
    data_vote_radar = vote_radar_data(vote_id)
    nb_voted_users_today = current_vote.nb_voted_users_today()
    string_names_has_voted_users_today=current_vote.string_names_has_voted_users_today()
    nb_not_voted_users_today = current_vote.nb_not_voted_users_today()
    string_names_not_has_voted_users_today = current_vote.string_names_not_has_voted_users_today()

    return render_template( "act/vote.html",
                           vote=current_vote,
                            data_vote_line_chart=data_vote_line_chart,
                            data_vote_radar=data_vote_radar,
                            random_option=random_option,
                            nb_voted_users_today=nb_voted_users_today,
                            string_names_has_voted_users_today=string_names_has_voted_users_today,
                            nb_not_voted_users_today=nb_not_voted_users_today,
                            string_names_not_has_voted_users_today=string_names_not_has_voted_users_today)

# 新增投票的选项
@bp.route("/vote/option/add/<vote_id>", methods=['GET', 'POST'])
@login_required
def vote_option_add(vote_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    option_names = current_vote.get_option_names()
    option = VoteOptionAddForm()
    if option.validate_on_submit():
        new_option = VoteOption(
            topic_id = vote_id,
            create_user = current_user.id,
            name = option.option_name.data
        )
        db.session.add(new_option)
        flash("成功添加餐馆\""+option.option_name.data+"\"")
        return redirect(url_for("act.vote", vote_id=vote_id))
    return render_template("act/vote_option_add.html", vote=current_vote,
                           option=option, option_names=option_names)


@bp.route("/vote/add/<vote_id>/<option_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def vote_option(vote_id, option_id, user_id):
    if db_add_vote(vote_id, option_id, user_id):
        flash("投票成功")
    return redirect(url_for("act.vote", vote_id=vote_id))


@bp.route("/vote/add_change/<vote_id>/<option_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def add_change_vote(vote_id, option_id, user_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    if current_vote.is_user_vote_today(user_id):
        db_delete_vote(vote_id, user_id)
    if db_add_vote(vote_id, option_id, user_id):
        flash("修改成功")
    return redirect(url_for("act.vote", vote_id=vote_id))


@bp.route("/vote/delete/<vote_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def delete_vote(vote_id, user_id):
    db_delete_vote(vote_id, user_id)
    flash("取消投票")
    return redirect(url_for("act.vote", vote_id=vote_id))

@bp.route("/vote/change/<vote_id>/<option_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def change_vote(vote_id, option_id, user_id):
    db_delete_vote(vote_id, user_id)
    db_add_vote(vote_id, option_id, user_id)
    flash("修改成功")
    return redirect(url_for("act.vote", vote_id=vote_id))

# 新增用户user_id对于投票id为vote_id的投票option_id
def db_delete_vote(vote_id, user_id):
    user_select = VoteOptionSelected.query.filter(
        and_(VoteOptionSelected.user_id == user_id,
             VoteOptionSelected.topic_id == vote_id)).all()
    for current_select in user_select:
        if current_select.create_time.date() == datetime.datetime.utcnow().date():
            db.session.delete(current_select)
    db.session.commit()

# 从数据库中删除用户user_id对于投票id为vote_id的投票option_id
def db_add_vote(vote_id, option_id, user_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    if not current_vote.is_user_vote_today(user_id):
        current_vote_option = VoteOption.query.filter_by(id=option_id).first()
        current_vote_option.user_vote(user_id)
        return True
    return False



