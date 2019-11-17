# 作者：hao.ren3
# 时间：2019/11/17 19:39
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField
from app.models.Tag import Tag
from wtforms.validators import DataRequired, Length, ValidationError

class TagForm(FlaskForm):
    tag = StringField("标签", validators=[
        DataRequired(), Length(min=1, max=20)])

    def validate_tag(self, tag):
        tag = Tag.query.filter_by(tag=tag.data).first()
        if tag is not None:
            raise ValidationError('当前标签已经被注册。')