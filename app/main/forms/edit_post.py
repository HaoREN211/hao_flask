# 作者：hao.ren3
# 时间：2019/11/11 16:28
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length


# 编辑帖子内容
class PostForm(FlaskForm):

    post = TextAreaField('帖子内容', validators=[
        DataRequired(), Length(min=1, max=16777215)])
    post_html = TextAreaField('帖子内容', validators=[
        DataRequired(), Length(min=1, max=16777215)])
    title = StringField('帖子标题', validators=[
        DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('确认修改')