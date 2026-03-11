from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.department = request.form.get('department', '')
        current_user.year = request.form.get('year', '')
        current_user.college = request.form.get('college', '')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('profile.html', user=current_user)
