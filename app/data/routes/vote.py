# 作者：hao.ren3
# 时间：2019/12/22 9:42
# IDE：PyCharm

from app.data import bp
from json import dumps
from app.models.Vote import VoteTopic
import datetime
from math import floor
from app.models.User import User

# 折线图数据，每日投票情况
@bp.route('/vote/<id>', methods=['POST'])
def vote(id):
    current_topic = VoteTopic.query.filter_by(id=id).first()
    max_date, min_date = current_topic.get_max_min_vote_date()

    list_date, list_data = list([]), list([])
    nb_date = (max_date-min_date).days + 1

    max_cnt = 0
    min_cnt = 9999
    interval = 5

    for current_index in range(nb_date):
        current_date = (min_date+datetime.timedelta(days=current_index)).strftime("%Y-%m-%d")
        nb_vote = current_topic.get_nb_vote_for_a_day(current_date)

        if nb_vote > max_cnt:
            max_cnt = nb_vote
        if nb_vote < min_cnt:
            min_cnt = nb_vote

        # 计算y轴刻度间距
        if (max_cnt-min_cnt) < 5:
            interval = 1
        else:
            interval = floor(float(max_cnt-min_cnt)/float(5))

        list_data.append(str(nb_vote))
        list_date.append('"'+current_date+'"')
    json_object = '{vote_cnt: ['+",".join(list_data)+'], vote_date:['+",".join(list_date)+'], max_cnt:'+str(max_cnt)+','\
                  +' min_cnt:'+str(min_cnt)+', interval:'+str(interval)+'}'
    return dumps(json_object)


# 雷达图，每人投票情况
@bp.route('/personal_vote/<id>', methods=['POST'])
def personal_vote(id):
    current_topic = VoteTopic.query.filter_by(id=id).first()
    list_colleague = User.query.filter_by(is_colleague=1).all()
    list_name, list_nb_vote, list_names_string = list([]), list([]), list([])
    nb_vote = 0

    for current_colleague in list_colleague:
        if (current_colleague.real_name is not None) and (current_colleague.real_name!=""):
            list_nb_vote.append(current_topic.user_vote_cnt(current_colleague.id))
            list_name.append(current_colleague.real_name)
            nb_vote += 1

    if nb_vote > 0:
        max_cnt = max(list_nb_vote)
        min_cnt = min(list_nb_vote)
        list_names_string = ['{name:"'+list_name[x]+'", max: '+str(max_cnt)+', min: '+str(min_cnt)+'}' for x in range(nb_vote)]

    list_nb_vote = [str(x) for x in list_nb_vote]

    json_object = '{list_name: ['+', '.join(list_names_string)+'], data:['+', '.join(list_nb_vote)+']}'
    return dumps(json_object)