from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.attendance import Attendance
from models.member import Member
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['GET', 'POST'])
@login_required
def manage_attendance():
    today = date.today()
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        time_in_str = request.form.get('time_in')
        time_in = datetime.strptime(time_in_str, '%H:%M').time() if time_in_str else None
        
        date_str = request.form.get('date')
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else today
        
        # check if member exists
        member = Member.query.filter_by(member_id=member_id).first()
        
        if not member:
            flash(f'No member found with ID {member_id}', 'danger')
        else:
            attendance = Attendance(
                member_id=member.id,
                date=attendance_date,
                time_in=time_in
            )
            db.session.add(attendance)
            try:
                db.session.commit()
                flash('Attendance marked successfully!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Attendance already marked for this member today.', 'warning')
            except Exception as e:
                db.session.rollback()
                flash(f'Error marking attendance: {str(e)}', 'danger')
                
        return redirect(url_for('attendance.manage_attendance'))
        
    # Get today's attendance
    records = Attendance.query.filter_by(date=today).order_by(Attendance.time_in.desc()).all()
    return render_template('admin/attendance.html', records=records, today=today)
