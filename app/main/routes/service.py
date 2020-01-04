# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2020/1/3 10:12
# IDE：PyCharm

import os
from app.main import bp
from app.main.forms.service import ServiceForm
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/service', methods=['GET', 'POST'])
@login_required
def service():
    if current_user.is_admin:
        services = get_all_service_list(is_linux=True)
        return render_template("service.html", services=services)
    else:
        return redirect(url_for("main.index"))





# 获取当前所有服务的pid端口号
def get_all_service_list(is_linux=True):
    list_services = list([])
    list_pid, is_active = find_pids_by_port(port=5000, is_linux=is_linux)
    list_services.append(
        ServiceForm(
            name="博客系统",
            port=5000,
            list_pid=list_pid,
            is_active=is_active
        )
    )
    list_pid, is_active = find_pids_by_port(port=5001, is_linux=is_linux)
    list_services.append(
        ServiceForm(
            name="企业信息",
            port=5001,
            list_pid=list_pid,
            is_active=is_active
        )
    )
    list_pid, is_active = find_pids_by_port(port=5002, is_linux=is_linux)
    list_services.append(
        ServiceForm(
            name="个人信息",
            port=5002,
            list_pid=list_pid,
            is_active=is_active
        )
    )
    return list_services


# 查看当前占用port端口号的服务pid
def find_pid_by_port(port, is_linux=True):
    if is_linux:
        result = os.popen("netstat -antp | grep 0.0.0.0.0:"+str(port)+" | awk '{print $7}' | awk -F/ '{print $1}'")
    else:
        result = os.popen('netstat -ano | findstr "0.0.0.0:'+str(port)+'"')
    res = result.read()
    list_pid = list([])
    for line in res.splitlines():
        list_pid.append(str(line).strip())
    return list_pid


# 查看当前占用port端口号的服务pid列表
def find_pids_by_port(port, is_linux=True):
    blog_service_pid = find_pid_by_port(port, is_linux)
    blog_service_pid = [str(x) for x in blog_service_pid]
    is_active = False
    list_pid = ",".join(blog_service_pid)
    if len(blog_service_pid) > 0:
        is_active = True
    return list_pid, is_active