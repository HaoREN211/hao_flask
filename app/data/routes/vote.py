# 作者：hao.ren3
# 时间：2019/12/22 9:42
# IDE：PyCharm

from app.data import bp
from json import dumps
from app.models.Vote import VoteTopic
import datetime
from math import floor

@bp.route('/vote/<id>', methods=['POST', 'GET'])
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
            interval = float(float(max_cnt-min_cnt)/float(5))

        list_data.append(str(nb_vote))
        list_date.append('"'+current_date+'"')
    json_object = '{vote_cnt: ['+",".join(list_data)+'], vote_date:['+",".join(list_date)+'], max_cnt:'+str(max_cnt)+','\
                  +' min_cnt:'+str(min_cnt)+', interval:'+str(interval)+'}'
    return dumps(json_object)