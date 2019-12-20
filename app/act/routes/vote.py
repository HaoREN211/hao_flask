# 作者：hao.ren3
# 时间：2019/12/20 9:36
# IDE：PyCharm

from app.act import bp
from app import db
from flask_login import login_required
from flask import render_template, flash
from app.models.Vote import VoteTopic, VoteOption, VoteOptionSelected
from operator import and_
from datetime import datetime

@bp.route("/vote/<vote_id>", methods=['GET', 'POST'])
@login_required
def vote(vote_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    return render_template("act/vote.html",
                           vote=current_vote)


@bp.route("/vote/add/<vote_id>/<option_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def vote_option(vote_id, option_id, user_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    if db_add_vote(vote_id, option_id, user_id):
        flash("投票成功")
    return render_template("act/vote.html",
                           vote=current_vote)


@bp.route("/vote/delete/<vote_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def delete_vote(vote_id, user_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    db_delete_vote(vote_id, user_id)
    flash("取消投票")
    return render_template("act/vote.html",
                           vote=current_vote)

@bp.route("/vote/change/<vote_id>/<option_id>/<user_id>", methods=['GET', 'POST'])
@login_required
def change_vote(vote_id, option_id, user_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    db_delete_vote(vote_id, user_id)
    db_add_vote(vote_id, option_id, user_id)
    flash("修改成功")
    return render_template("act/vote.html",
                           vote=current_vote)


def db_delete_vote(vote_id, user_id):
    user_select = VoteOptionSelected.query.filter(
        and_(VoteOptionSelected.user_id == user_id,
             VoteOptionSelected.topic_id == vote_id)).all()
    for current_select in user_select:
        if current_select.create_time.date() == datetime.utcnow().date():
            db.session.delete(current_select)
    db.session.commit()

def db_add_vote(vote_id, option_id, user_id):
    current_vote = VoteTopic.query.filter_by(id=vote_id).first()
    if not current_vote.is_user_vote_today(user_id):
        current_vote_option = VoteOption.query.filter_by(id=option_id).first()
        current_vote_option.user_vote(user_id)
        return True
    return False