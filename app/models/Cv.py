# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/29 10:13
# IDE：PyCharm

from app import db
from sqlalchemy.dialects.mysql import BIGINT
from datetime import datetime

class Cv(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="简历主键")
    name = db.Column(db.String(100), nullable=False, comment="简历名称")
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("user.id"), comment="作者主键")
    is_delete = db.Column(db.Boolean, default=False, comment="是否删除")
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.utcnow(), comment="更新时间")
    delete_time = db.Column(db.DateTime, comment="删除时间")

    author = db.relationship('User', backref='cvs')
    main_attributes = db.relationship('CvMainAttribute', backref='cv')
    schools = db.relationship('CvSchool', backref='cv')


    # 新增主属性的order值
    def calculate_max_main_attribute_order(self):
        if len(self.main_attributes) == 0:
            return 1
        list_attribute_order = [x.order for x in self.main_attributes]
        return max(list_attribute_order)+1


class CvMainAttribute(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="简历主属性主键")
    cv_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("cv.id"), comment="简历主键", nullable=False)
    order = db.Column(db.Integer, comment="主属性顺序")
    name = db.Column(db.String(100), nullable=False, comment="简历主属性键")
    value = db.Column(db.String(100), nullable=False, comment="简历主属性值")

class CvSchool(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="简历学校主键")
    cv_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("cv.id"), comment="简历主键", nullable=False)
    name = db.Column(db.String(100), nullable=False, comment="学校名称")
    image_link = db.Column(db.String(500), comment="学校图片链接")
    start_time = db.Column(db.Date, comment="入学时间")
    end_time = db.Column(db.Date, comment="毕业时间")
    level = db.Column(db.String(20), comment="学历")