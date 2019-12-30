# -*- coding: UTF-8 -*- 
# 作者：hao.ren3
# 时间：2019/12/29 10:00
# IDE：PyCharm

from app.data import bp
from app import db
from flask_login import login_required, current_user
from flask import render_template, request, url_for, redirect
from app.models.Cv import Cv, CvMainAttribute
from config import Config
from app.data.forms.Cv import CvMainAttributeForm, CvSchoolForm

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
    cv_school = CvSchoolForm()

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
    if cv_school.validate_on_submit():
        return redirect(url_for("data.cv", id=current_cv.id))
    return render_template("data/cv.html", cv=current_cv,
                           cv_main_attribute_form=cv_main_attribute_form,
                           cv_school=cv_school)
