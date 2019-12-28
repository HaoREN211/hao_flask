# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/28 9:31
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired

class VoteOptionAddForm(FlaskForm):
    vote_id = IntegerField("投票主题ID", validators=[DataRequired()])
    user_id = IntegerField("用户主键ID", validators=[DataRequired()])
    option_name = StringField("餐馆名称", validators=[DataRequired()])
