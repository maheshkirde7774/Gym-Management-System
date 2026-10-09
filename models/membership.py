from . import db
from datetime import datetime

class Membership(db.Model):
    __tablename__ = 'memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plans.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    amount_total = db.Column(db.Numeric(10, 2), nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def amount_pending(self):
        return self.amount_total - self.amount_paid
        
    @property
    def payment_status(self):
        if self.amount_paid >= self.amount_total:
            return 'Paid'
        elif self.amount_paid > 0:
            return 'Partial'
        return 'Pending'
