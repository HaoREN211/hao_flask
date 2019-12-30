# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/29 9:59
# IDE：PyCharm

from flask import Blueprint

bp = Blueprint('data', __name__)

from app.data.routes import cv