# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/29 10:00
# IDE：PyCharm

from app.data import bp
from app import db
from flask_login import login_required, current_user
from flask import render_template, request, url_for, redirect
from app.models.Cv import Cv, CvMainAttribute, CvSchool, CvEnterprise, CvResponsibility
from config import Config
from app.data.forms.Cv import CvMainAttributeForm, CvSchoolForm, CvEnterpriseForm, CvResponsibilityForm

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
        to_add = CvEnterprise(
            cv_id=id,
            name=cv_enterprise_form.name.data,
            image_link=cv_enterprise_form.image_link.data,
            is_active=cv_enterprise_form.is_active.data,
            start_time=cv_enterprise_form.start_time.data,
            end_time=cv_enterprise_form.end_time.data,
            position=cv_enterprise_form.position.data,
            location=cv_enterprise_form.location.data
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
    return render_template("data/cv.html", cv=current_cv, is_edited=is_edited,
                           cv_main_attribute_form=cv_main_attribute_form,
                           cv_school_form=cv_school_form,
                           cv_enterprise_form=cv_enterprise_form,
                           cv_responsibility_form=cv_responsibility_form)


@bp.route('/cv/edit/<id>', methods=['GET', 'POST'])
def cv_edit(id):
    current_cv = Cv.query.filter_by(id=id).first()
    cv_main_attribute_form = CvMainAttributeForm()
    cv_school_form = CvSchoolForm()
    cv_enterprise_form = CvEnterpriseForm()
    cv_responsibility_form = CvResponsibilityForm()
    is_edited = True

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
        to_add = CvEnterprise(
            cv_id=id,
            name=cv_enterprise_form.name.data,
            image_link=cv_enterprise_form.image_link.data,
            is_active=cv_enterprise_form.is_active.data,
            start_time=cv_enterprise_form.start_time.data,
            end_time=cv_enterprise_form.end_time.data,
            position=cv_enterprise_form.position.data,
            location=cv_enterprise_form.location.data
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
    return render_template("data/cv.html", cv=current_cv, is_edited=is_edited,
                           cv_main_attribute_form=cv_main_attribute_form,
                           cv_school_form=cv_school_form,
                           cv_enterprise_form=cv_enterprise_form,
                           cv_responsibility_form=cv_responsibility_form)