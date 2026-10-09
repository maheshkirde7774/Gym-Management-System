from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.member import Member
from models.plan import MembershipPlan
from models.membership import Membership
import uuid
from datetime import datetime

members_bp = Blueprint('members', __name__)

@members_bp.route('/')
@login_required
def list_members():
    search = request.args.get('search', '')
    if search:
        members = Member.query.filter(
            (Member.first_name.ilike(f'%{search}%')) | 
            (Member.last_name.ilike(f'%{search}%')) |
            (Member.member_id.ilike(f'%{search}%'))
        ).all()
    else:
        members = Member.query.order_by(Member.created_at.desc()).all()
    return render_template('admin/members.html', members=members, search=search)

@members_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_member():
    if request.method == 'POST':
        # generate member ID
        member_id = f"GYM-{uuid.uuid4().hex[:6].upper()}"
        
        member = Member(
            member_id=member_id,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            gender=request.form.get('gender')
        )
        
        dob_str = request.form.get('dob')
        if dob_str:
            member.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            
        join_date_str = request.form.get('join_date')
        if join_date_str:
            member.join_date = datetime.strptime(join_date_str, '%Y-%m-%d').date()
            
        db.session.add(member)
        
        try:
            db.session.commit()
            flash('Member added successfully!', 'success')
            return redirect(url_for('members.list_members'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding member: {str(e)}', 'danger')
            
    return render_template('admin/member_form.html', member=None)

@members_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_member(id):
    member = Member.query.get_or_404(id)
    
    if request.method == 'POST':
        member.first_name = request.form.get('first_name')
        member.last_name = request.form.get('last_name')
        member.email = request.form.get('email')
        member.phone = request.form.get('phone')
        member.address = request.form.get('address')
        member.gender = request.form.get('gender')
        
        dob_str = request.form.get('dob')
        if dob_str:
            member.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            
        join_date_str = request.form.get('join_date')
        if join_date_str:
            member.join_date = datetime.strptime(join_date_str, '%Y-%m-%d').date()
            
        try:
            db.session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('members.list_members'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating member: {str(e)}', 'danger')
            
    return render_template('admin/member_form.html', member=member)

@members_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    member = Member.query.get_or_404(id)
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    return render_template('admin/member_profile.html', member=member, plans=plans)

@members_bp.route('/<int:id>/add_membership', methods=['POST'])
@login_required
def add_membership(id):
    member = Member.query.get_or_404(id)
    plan_id = request.form.get('plan_id')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    plan = MembershipPlan.query.get_or_404(plan_id)
    
    membership = Membership(
        member_id=member.id,
        plan_id=plan.id,
        start_date=start_date,
        end_date=end_date,
        amount_total=plan.price
    )
    
    db.session.add(membership)
    db.session.commit()
    flash('Membership added successfully', 'success')
    return redirect(url_for('members.profile', id=member.id))
