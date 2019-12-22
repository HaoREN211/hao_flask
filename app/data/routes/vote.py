# 作者：hao.ren3
# 时间：2019/12/22 9:42
# IDE：PyCharm

from app.data import bp
from json import dumps
from app.models.Vote import VoteTopic
import datetime

@bp.route('/vote/<id>', methods=['POST', 'GET'])
def vote(id):
    current_topic = VoteTopic.query.filter_by(id=id).first()
    max_date, min_date = current_topic.get_max_min_vote_date()

    list_date, list_data = list([]), list([])
    nb_date = (max_date-min_date).days + 1

    for current_index in range(nb_date):
        current_date = (min_date+datetime.timedelta(days=current_index)).strftime("%Y-%m-%d")
        list_data.append(str(current_topic.get_nb_vote_for_a_day(current_date)))
        list_date.append('"'+current_date+'"')

    json_object = '{vote_cnt: ['+",".join(list_data)+'], vote_date:['+",".join(list_date)+']}'
    return dumps(json_object)