# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/3 13:55
# IDE：PyCharm

import os

def kill_service(port):
    result = os.popen("netstat -antp | grep 0.0.0.0.0:" + str(port) + " | awk '{print $7}' | awk -F/ '{print $1}'")
    res = result.read()
    for line in res.splitlines():
        current_pid = str(line).strip()
        os.popen("kill "+current_pid)

if __name__ == '__main__':
    kill_service(5000)
    kill_service(5001)
    kill_service(5002)

