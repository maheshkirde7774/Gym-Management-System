from flask import Blueprint, render_template
from flask_login import login_required
from models.member import Member
from models.payment import Payment
from models.attendance import Attendance
from sqlalchemy import func
from models import db
from datetime import date

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def dashboard():
    # Calculate statistics
    total_members = Member.query.count()
    
    # Active members (members with an active membership)
    members = Member.query.all()
    active_members = sum(1 for m in members if m.is_active)
    expired_memberships = total_members - active_members
    
    # Today's attendance
    today = date.today()
    todays_attendance = Attendance.query.filter_by(date=today).count()
    
    # Monthly revenue
    current_month = today.month
    current_year = today.year
    monthly_revenue = db.session.query(func.sum(Payment.amount)).filter(
        func.extract('month', Payment.payment_date) == current_month,
        func.extract('year', Payment.payment_date) == current_year
    ).scalar() or 0
    
    return render_template('admin/dashboard.html', 
                          total_members=total_members,
                          active_members=active_members,
                          expired_memberships=expired_memberships,
                          todays_attendance=todays_attendance,
                          monthly_revenue=monthly_revenue)
