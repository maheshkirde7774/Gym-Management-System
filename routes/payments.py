from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.payment import Payment
from models.membership import Membership
from models.member import Member
import uuid
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/')
@login_required
def list_payments():
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', payments=payments)

@payments_bp.route('/add/<int:membership_id>', methods=['GET', 'POST'])
@login_required
def add_payment(membership_id):
    membership = Membership.query.get_or_404(membership_id)
    member = Member.query.get_or_404(membership.member_id)
    
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        if amount <= 0:
            flash('Payment amount must be greater than zero.', 'danger')
            return redirect(url_for('payments.add_payment', membership_id=membership.id))
            
        if amount > membership.amount_pending:
            flash('Payment amount cannot exceed pending amount.', 'danger')
            return redirect(url_for('payments.add_payment', membership_id=membership.id))
            
        transaction_id = request.form.get('transaction_id')
        if not transaction_id:
            transaction_id = f"TRX-{uuid.uuid4().hex[:8].upper()}"
            
        payment_date_str = request.form.get('payment_date')
        payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d').date() if payment_date_str else datetime.today().date()
        
        payment = Payment(
            member_id=member.id,
            amount=amount,
            payment_date=payment_date,
            payment_method=request.form.get('payment_method'),
            transaction_id=transaction_id
        )
        
        # update membership paid amount
        membership.amount_paid += amount
        
        db.session.add(payment)
        db.session.commit()
        
        flash('Payment recorded successfully!', 'success')
        return redirect(url_for('members.profile', id=member.id))
        
    return render_template('admin/payment_form.html', membership=membership, member=member)
