from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.plan import MembershipPlan

plans_bp = Blueprint('plans', __name__)

@plans_bp.route('/')
@login_required
def list_plans():
    plans = MembershipPlan.query.all()
    return render_template('admin/plans.html', plans=plans)

@plans_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_plan():
    if request.method == 'POST':
        plan = MembershipPlan(
            name=request.form.get('name'),
            description=request.form.get('description'),
            duration_months=request.form.get('duration_months'),
            price=request.form.get('price'),
            is_active=True if request.form.get('is_active') == 'on' else False
        )
        db.session.add(plan)
        db.session.commit()
        flash('Plan created successfully!', 'success')
        return redirect(url_for('plans.list_plans'))
        
    return render_template('admin/plan_form.html', plan=None)

@plans_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_plan(id):
    plan = MembershipPlan.query.get_or_404(id)
    
    if request.method == 'POST':
        plan.name = request.form.get('name')
        plan.description = request.form.get('description')
        plan.duration_months = request.form.get('duration_months')
        plan.price = request.form.get('price')
        plan.is_active = True if request.form.get('is_active') == 'on' else False
        
        db.session.commit()
        flash('Plan updated successfully!', 'success')
        return redirect(url_for('plans.list_plans'))
        
    return render_template('admin/plan_form.html', plan=plan)
