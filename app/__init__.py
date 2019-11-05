# 作者：hao.ren3
# 时间：2019/11/5 14:33
# IDE：PyCharm

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
