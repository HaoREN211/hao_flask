# 作者：hao.ren3
# 时间：2019/11/11 14:51
# IDE：PyCharm

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from config import TranslateLoginForm



# 登录界面
class LoginForm(FlaskForm):
    username = StringField(TranslateLoginForm.Username, validators=[DataRequired()])
    password = PasswordField(TranslateLoginForm.Password, validators=[DataRequired()])
    remember_me = BooleanField(TranslateLoginForm.RememberMe)
    submit = SubmitField(TranslateLoginForm.submit)