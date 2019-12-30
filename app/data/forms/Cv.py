# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/29 20:05
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, IntegerField
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
    level = StringField("学位学历", validators=[DataRequired()])
    specialty = StringField("学习专业", validators=[DataRequired()])
    submit = SubmitField("确认")

class CvEnterpriseForm(FlaskForm):
    name = StringField("公司名称", validators=[DataRequired()])
    image_link = StringField("公司LoGo链接")
    is_active = BooleanField("当前是否在职")
    start_time = DateField("入职时间", validators=[DataRequired()])
    end_time = DateField("离职时间", validators=[DataRequired()])
    position = StringField("职位", validators=[DataRequired()])
    location = StringField("工作地点", validators=[DataRequired()])
    submit = SubmitField("确认")


class CvResponsibilityForm(FlaskForm):
    enterprise_id = IntegerField("公司主键", validators=[DataRequired()])
    name = StringField("工作职责描述", validators=[DataRequired()])
    submit = SubmitField("确认")


class CvProjectForm(FlaskForm):
    enterprise_id = IntegerField("公司主键", validators=[DataRequired()])
    name = StringField("项目名称", validators=[DataRequired()])
    role = StringField("职位职责", validators=[DataRequired()])
    start_time = DateField("入职时间", validators=[DataRequired()])
    end_time = DateField("离职时间", validators=[DataRequired()])
    submit = SubmitField("确认")
