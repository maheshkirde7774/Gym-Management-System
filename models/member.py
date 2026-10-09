from . import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(20), unique=True, nullable=False) # e.g., GYM-2023-0001
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.Text, nullable=True)
    join_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    memberships = db.relationship('Membership', backref='member', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='member', lazy=True, cascade='all, delete-orphan')
    attendance = db.relationship('Attendance', backref='member', lazy=True, cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        
    @property
    def current_membership(self):
        # Return the latest active membership
        from datetime import date
        today = date.today()
        # Find membership where end_date >= today
        for m in sorted(self.memberships, key=lambda x: x.end_date, reverse=True):
            if m.start_date <= today <= m.end_date:
                return m
        # If no active, return latest
        if self.memberships:
            return sorted(self.memberships, key=lambda x: x.end_date, reverse=True)[0]
        return None
        
    @property
    def is_active(self):
        m = self.current_membership
        from datetime import date
        if m and m.start_date <= date.today() <= m.end_date:
            return True
        return False
