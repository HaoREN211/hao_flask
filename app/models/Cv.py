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
    enterprises = db.relationship('CvEnterprise', backref='cv')
    projects = db.relationship('CvProject', backref='cv')


    # 新增主属性的order值
    def calculate_max_main_attribute_order(self):
        if len(self.main_attributes) == 0:
            return 1
        list_attribute_order = [x.order for x in self.main_attributes]
        return max(list_attribute_order)+1

    # 获取以入学时间从晚到早排序的学校列表
    def get_start_time_ordered_schools(self):
        list_schools = self.schools
        return sorted(list_schools, key=lambda x:x.start_time, reverse=True)

    # 获取以入职时间从晚到早排序的公司列表
    def get_start_time_ordered_enterprises(self):
        list_enterprises = self.enterprises
        list_enterprises = list(filter(lambda x: x.is_internship == False, list_enterprises))
        return sorted(list_enterprises, key=lambda x: x.start_time, reverse=True)

    # 获取以入职时间从晚到早排序的实习公司列表
    def get_start_time_ordered_internship(self):
        list_enterprises = self.enterprises
        list_enterprises = list(filter(lambda x: x.is_internship == True, list_enterprises))
        return sorted(list_enterprises, key=lambda x: x.start_time, reverse=True)

    # 获取以入职时间从晚到早排序的项目列表
    def get_start_time_ordered_project(self):
        list_projects = self.projects
        return sorted(list_projects, key=lambda x: x.start_time, reverse=True)


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
    specialty = db.Column(db.String(20), comment="专业")

class CvEnterprise(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="简历工作经历主键")
    cv_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("cv.id"), comment="简历主键", nullable=False)
    name = db.Column(db.String(100), nullable=False, comment="公司名称名称")
    image_link = db.Column(db.String(500), comment="公司LoGo链接")
    is_active = db.Column(db.Boolean, comment="当前是否在职")
    start_time = db.Column(db.Date, comment="入职时间")
    end_time = db.Column(db.Date, comment="离职时间")
    position = db.Column(db.String(100), comment="职位")
    location = db.Column(db.String(100), comment="工作地点")
    is_internship = db.Column(db.Boolean, default=False, comment="是否是实习经验")

    responsibilities = db.relationship('CvResponsibility', backref='enterprise')

    # 新增工作职责的order值
    def calculate_max_main_responsibility_order(self):
        if len(self.responsibilities) == 0:
            return 1
        list_responsibility_order = [x.order for x in self.responsibilities]
        return max(list_responsibility_order) + 1


    # 获取按照顺序排列的职责列表
    def get_ordered_responsibilities(self):
        return sorted(self.responsibilities, key=lambda x: x.order, reverse=False)

class CvResponsibility(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="简历工作经验主键")
    cv_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("cv.id"), comment="简历主键", nullable=False)
    enterprise_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("cv_enterprise.id"), comment="简历公司主键", nullable=False)
    order = db.Column(db.Integer, comment="工作责任顺序顺序")
    name = db.Column(db.String(200), comment="工作职责描述")

class CvProject(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True, comment="简历项目主键")
    cv_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("cv.id"), comment="简历主键", nullable=False)
    enterprise_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("cv_enterprise.id"), comment="公司主键", nullable=False)
    name = db.Column(db.String(100), nullable=False, comment="项目名称")
    role = db.Column(db.String(100), comment="职位")
    start_time = db.Column(db.Date, comment="开始时间")
    end_time = db.Column(db.Date, comment="结束时间")