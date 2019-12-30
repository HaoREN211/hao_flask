# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/29 20:05
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

class CvMainAttributeForm(FlaskForm):
    attribute_key = StringField("属性键", validators=[DataRequired()])
    attribute_value = StringField("属性值", validators=[DataRequired()])
    submit = SubmitField("确认")

class CvSchoolForm(FlaskForm):
    name = StringField("学校名称", validators=[DataRequired()])
    image_link = StringField("学校图片链接")
    start_time = DateField("入学时间", validators=[DataRequired()])
    end_time = DateField("毕业时间", validators=[DataRequired()])
    level = StringField("学历")
    submit = SubmitField("确认")

