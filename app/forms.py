# 作者：hao.ren3
# 时间：2019/11/5 17:01
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from config import TranslateLoginForm

class LoginForm(FlaskForm):
    username = StringField(TranslateLoginForm.Username, validators=[DataRequired()])
    password = PasswordField(TranslateLoginForm.Password, validators=[DataRequired()])
    remember_me = BooleanField(TranslateLoginForm.RememberMe)
    submit = SubmitField(TranslateLoginForm.submit)