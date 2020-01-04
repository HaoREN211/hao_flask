# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/3 11:01
# IDE：PyCharm

class ServiceForm(object):
    def __init__(self, name, port, list_pid, is_active):
        self.name = name
        self.port = port
        self.list_pid=list_pid
        self.is_active = is_active
