# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/27 22:05
# IDE：PyCharm

class VoteLineChartData(object):
    def __init__(self, vote_cnt, vote_date, max_cnt, min_cnt, interval):
        self.vote_cnt = vote_cnt
        self.vote_date = vote_date
        self.max_cnt = max_cnt
        self.min_cnt = min_cnt
        self.interval = interval


class VoteRadarData(object):
    def __init__(self, list_name, data):
        self.list_name = list_name
        self.data = data