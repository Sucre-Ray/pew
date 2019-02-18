from app import db
from app.user import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.user.forms import EditProfileForm
from app.auth.forms import ChangePasswordForm
from app.models import User


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile_form = EditProfileForm()
    password_form = ChangePasswordForm()
    if profile_form.validate_on_submit():
        current_user.name = profile_form.name.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        profile_form.name.data = current_user.name
        profile_form.bio.data = current_user.bio
    elif password_form.validate_on_submit():
        # user = User.query.filter_by(email=current_user.email).first()
        if not current_user.check_password(password_form.old_password.data):
            flash('Old password is incorrect.')
            return redirect(url_for('user.edit_profile'))
        current_user.set_password(password_form.new_password.data)
        db.session.commit()
        flash('Your password successfully changed.')
        return redirect(url_for('user.edit_profile'))
    return render_template('user/edit_profile.html',
                           title='Edit Profile',
                           profile_form=profile_form,
                           password_form=password_form,
                           user=current_user)


@bp.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('user/user.html', user=user)


