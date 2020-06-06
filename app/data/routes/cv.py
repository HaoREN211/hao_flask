# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2019/12/29 10:00
# IDE：PyCharm

from config import wkhtmltopdf_path
from app.data import bp
from app import db
from flask_login import login_required, current_user
from flask import render_template, request, url_for, redirect, current_app, send_from_directory
from app.models.Cv import Cv, CvMainAttribute, CvSchool, CvEnterprise, CvResponsibility, CvProject, CvExperience
from config import Config
from app.data.forms.Cv import (CvMainAttributeForm, CvSchoolForm, CvEnterpriseForm, CvResponsibilityForm,
                               CvProjectForm, CvExperienceForm)
import pdfkit
import os

@bp.route('/cv_export/<id>', methods=['GET', 'POST'])
def cv_export(id):
    file_path = os.path.join(current_app.root_path, "static/cv/cv_REN_Hao_" + str(id) + ".pdf")
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    if os.path.exists(file_path):
        os.remove(file_path)
    url="127.0.0.1:5000"+str(url_for("data.cv", id=id))

    pdfkit.from_url(url,
                    file_path,
                    configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))
    return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path), as_attachment=True)


@bp.route('/cvs', methods=['GET', 'POST'])
@login_required
def cvs():
    current_user_id = current_user.id

    # 分页功能
    page = request.args.get('page', 1, type=int)
    cvs = Cv.query.filter_by(user_id=current_user_id).paginate(
        page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('data.cv', page=cvs.next_num) if cvs.has_next else None
    prev_url = url_for('data.cv', page=cvs.prev_num) if cvs.has_prev else None

    return render_template("data/cvs.html",
                           cvs = cvs.items,
                           next_url=next_url,
                           prev_url=prev_url)

@bp.route('/cv/<id>', methods=['GET', 'POST'])
def cv(id):
    current_cv = Cv.query.filter_by(id=id).first()
    cv_main_attribute_form = CvMainAttributeForm()
    cv_school_form = CvSchoolForm()
    cv_enterprise_form = CvEnterpriseForm()
    cv_responsibility_form = CvResponsibilityForm()
    cv_project_form = CvProjectForm(id)
    is_edited = False

    if cv_main_attribute_form.validate_on_submit():
        new_order_id = current_cv.calculate_max_main_attribute_order()
        to_add = CvMainAttribute(
            cv_id=id,
            order=new_order_id,
            name=cv_main_attribute_form.attribute_key.data,
            value=cv_main_attribute_form.attribute_value.data
        )
        db.session.add(to_add)
        return redirect(url_for("data.cv", id=current_cv.id))
    if cv_school_form.validate_on_submit():
        to_add = CvSchool(
            cv_id=id,
            name=cv_school_form.name.data,
            image_link=cv_school_form.image_link.data,
            start_time=cv_school_form.start_time.data,
            end_time=cv_school_form.end_time.data,
            level=cv_school_form.level.data,
            specialty=cv_school_form.specialty.data
        )
        db.session.add(to_add)
        return redirect(url_for("data.cv", id=current_cv.id))

    if cv_enterprise_form.validate_on_submit():
        is_internship = False
        if cv_enterprise_form.is_internship.data == 1:
            is_internship = True
        to_add = CvEnterprise(
            cv_id=id,
            name=cv_enterprise_form.name.data,
            image_link=cv_enterprise_form.image_link.data,
            is_active=cv_enterprise_form.is_active.data,
            start_time=cv_enterprise_form.start_time.data,
            end_time=cv_enterprise_form.end_time.data,
            position=cv_enterprise_form.position.data,
            location=cv_enterprise_form.location.data,
            is_internship=is_internship
        )
        db.session.add(to_add)
        return redirect(url_for("data.cv", id=current_cv.id))
    if cv_responsibility_form.validate_on_submit():
        current_enterprise_id = cv_responsibility_form.enterprise_id.data
        current_enterprise = CvEnterprise.query.filter_by(id=current_enterprise_id).first()
        new_order_id = current_enterprise.calculate_max_main_responsibility_order()
        to_add = CvResponsibility(
            cv_id=id,
            enterprise_id=current_enterprise_id,
            order=new_order_id,
            name=cv_responsibility_form.name.data,
        )
        db.session.add(to_add)
        return redirect(url_for("data.cv", id=current_cv.id))

    if cv_project_form.is_submitted():
        print("------- cv_project_form")
        if cv_project_form.validate_on_submit():
            print("valid")
        else:
            print(cv_project_form.errors)
        print(cv_project_form.enterprise_id.data)
        print(cv_project_form.name.data)
        print(cv_project_form.role.data)
        print(cv_project_form.start_time.data)
        print(cv_project_form.end_time.data)

    if cv_project_form.validate_on_submit():
        to_add = CvProject(
            cv_id=id,
            enterprise_id=cv_project_form.enterprise_id.data,
            name=cv_project_form.name.data,
            role=cv_project_form.role.data,
            start_time=cv_project_form.start_time.data,
            end_time = cv_project_form.end_time.data
        )
        db.session.add(to_add)
        return redirect(url_for("data.cv", id=current_cv.id))
    return render_template("data/cv.html", current_cv=current_cv, is_edited=is_edited,
                           cv_main_attribute_form=cv_main_attribute_form,
                           cv_school_form=cv_school_form,
                           cv_enterprise_form=cv_enterprise_form,
                           cv_responsibility_form=cv_responsibility_form,
                           cv_project_form=cv_project_form)


@bp.route('/cv/edit/<id>', methods=['GET', 'POST'])
def cv_edit(id):
    current_cv = Cv.query.filter_by(id=id).first()
    cv_main_attribute_form = CvMainAttributeForm()
    cv_school_form = CvSchoolForm()
    cv_enterprise_form = CvEnterpriseForm()
    cv_responsibility_form = CvResponsibilityForm()
    cv_project_form = CvProjectForm()
    list_enterprises = CvEnterprise.query.filter_by(cv_id=id).all()
    cv_project_form.enterprise_id.choices = [(x.id, x.name) for x in list_enterprises]
    cv_experience_form = CvExperienceForm()
    is_edited = True

    if is_form_validate_on_submit(current_cv, cv_main_attribute_form, cv_school_form, cv_enterprise_form
                               , cv_responsibility_form, cv_project_form, cv_experience_form):
        return redirect(url_for("data.cv_edit", id=current_cv.id))
    return render_template("data/cv.html", current_cv=current_cv, is_edited=is_edited,
                           cv_main_attribute_form=cv_main_attribute_form,
                           cv_school_form=cv_school_form,
                           cv_enterprise_form=cv_enterprise_form,
                           cv_responsibility_form=cv_responsibility_form,
                           cv_project_form=cv_project_form,
                           cv_experience_form=cv_experience_form)


# 只要有一个表单提交，则做相应的数据库修改，并重定向到修改界面
def is_form_validate_on_submit(current_cv, cv_main_attribute_form, cv_school_form, cv_enterprise_form
                               , cv_responsibility_form, cv_project_form, cv_experience_form):
    if cv_project_form.validate_on_submit():
        current_app.logger.info("简历模块：收到简历项目提交表单《"+cv_project_form.name.data+"》")
        cv_project_form_validate_on_submit(current_cv, cv_project_form)
        return True
    if cv_experience_form.validate_on_submit():
        current_app.logger.info("简历模块：收到项目经验提交表单《" + cv_experience_form.name.data + "》")
        cv_experience_form_validate_on_submit(current_cv, cv_experience_form)
        return True
    if cv_main_attribute_form.validate_on_submit():
        current_app.logger.info("简历模块：收到主要属性提交表单《" + cv_main_attribute_form.attribute_value.data + "》")
        cv_main_attribute_form_validate_on_submit(current_cv, cv_main_attribute_form)
        return True
    if cv_school_form.validate_on_submit():
        current_app.logger.info("简历模块：收到教育经历提交表单《" + cv_school_form.name.data + "》")
        cv_school_form_validate_on_submit(current_cv, cv_school_form)
        return True
    if cv_enterprise_form.validate_on_submit():
        current_app.logger.info("简历模块：收到工作经历提交表单《" + cv_enterprise_form.name.data + "》")
        cv_enterprise_form_validate_on_submit(current_cv, cv_enterprise_form)
        return True
    if cv_responsibility_form.validate_on_submit():
        current_app.logger.info("简历模块：收到工作职责提交表单《" + cv_responsibility_form.name.data + "》")
        cv_responsibility_form_validate_on_submit(current_cv, cv_responsibility_form)
        return True
    return False


# 新增主要属性表单提交
def cv_main_attribute_form_validate_on_submit(current_cv, cv_main_attribute_form):
    new_order_id = current_cv.calculate_max_main_attribute_order()
    to_add = CvMainAttribute(
        cv_id=current_cv.id,
        order=new_order_id,
        name=cv_main_attribute_form.attribute_key.data,
        value=cv_main_attribute_form.attribute_value.data
    )
    db.session.add(to_add)


# 新增教育经历表单提交
def cv_school_form_validate_on_submit(current_cv, cv_school_form):
    to_add = CvSchool(
        cv_id=current_cv.id,
        name=cv_school_form.name.data,
        image_link=cv_school_form.image_link.data,
        start_time=cv_school_form.start_time.data,
        end_time=cv_school_form.end_time.data,
        level=cv_school_form.level.data,
        specialty=cv_school_form.specialty.data
    )
    db.session.add(to_add)


# 新增工作经历和实习经历表单提交
def cv_enterprise_form_validate_on_submit(current_cv, cv_enterprise_form):
    is_internship = False
    if int(cv_enterprise_form.is_internship.data) == 1:
        is_internship = True
    to_add = CvEnterprise(
        cv_id=current_cv.id,
        name=cv_enterprise_form.name.data,
        image_link=cv_enterprise_form.image_link.data,
        is_active=cv_enterprise_form.is_active.data,
        start_time=cv_enterprise_form.start_time.data,
        end_time=cv_enterprise_form.end_time.data,
        position=cv_enterprise_form.position.data,
        location=cv_enterprise_form.location.data,
        is_internship=is_internship
    )
    db.session.add(to_add)


# 新增工作和实习职责表单提交
def cv_responsibility_form_validate_on_submit(current_cv, cv_responsibility_form):
    current_enterprise_id = cv_responsibility_form.enterprise_id.data
    current_enterprise = CvEnterprise.query.filter_by(id=current_enterprise_id).first()
    new_order_id = current_enterprise.calculate_max_main_responsibility_order()
    to_add = CvResponsibility(
        cv_id=current_cv.id,
        enterprise_id=current_enterprise_id,
        order=new_order_id,
        name=cv_responsibility_form.name.data,
    )
    db.session.add(to_add)


# 新增项目表单提交
def cv_project_form_validate_on_submit(current_cv, cv_project_form):
    to_add = CvProject(
        cv_id=current_cv.id,
        enterprise_id=cv_project_form.enterprise_id.data,
        name=cv_project_form.name.data,
        role=cv_project_form.role.data,
        start_time=cv_project_form.start_time.data,
        end_time=cv_project_form.end_time.data
    )
    db.session.add(to_add)


# 新增项目经验
def cv_experience_form_validate_on_submit(current_cv, cv_experience_form):
    current_project = CvProject.query.filter_by(id=int(cv_experience_form.project_id.data)).first()
    new_order = current_project.calculate_max_main_experience_order()
    to_add = CvExperience(
        cv_id = current_cv.id,
        enterprise_id = int(cv_experience_form.enterprise_id.data),
        project_id = int(cv_experience_form.project_id.data),
        order = new_order,
        name = cv_experience_form.name.data
    )
    db.session.add(to_add)