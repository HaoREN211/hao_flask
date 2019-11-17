# 作者：hao.ren3
# 时间：2019/11/11 16:28
# IDE：PyCharm
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from app.models.Tag import Tag

# 编辑帖子内容
class PostForm(FlaskForm):
    post = TextAreaField('帖子内容', validators=[
        DataRequired(), Length(min=1, max=16777215)])
    title = StringField('帖子标题', validators=[
        DataRequired(), Length(min=1, max=200)])
    list_tags = SelectMultipleField('标签', choices=[("1", 'python')])
    submit = SubmitField('确认修改')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.list_tags.choices = [(str(b.id), b.tag) for b in Tag.query.all()]

