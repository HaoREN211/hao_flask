# 作者：hao.ren3
# 时间：2019/11/11 16:25
# IDE：PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.model import User


# 注册新用户
class RegistrationForm(FlaskForm):
    username = StringField('用户名:', validators=[DataRequired()])
    email = StringField('邮箱地址:', validators=[DataRequired(), Email()])
    password = PasswordField('密码:', validators=[DataRequired()])
    password2 = PasswordField(
        '确认密码:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('点击注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('当前用户名已被占用，请使用另外一个用户名。')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('当前邮箱地址已被占用，请使用另外一个邮箱地址')
