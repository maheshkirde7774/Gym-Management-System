from app import create_app
from models import db
from models.user import User
from models.plan import MembershipPlan
from models.member import Member
from models.trainer import Trainer
from models.membership import Membership
from models.payment import Payment
from models.attendance import Attendance
from datetime import date, timedelta, datetime
import uuid

app = create_app()

def seed_data():
    with app.app_context():
        # Check if admin exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("Admin user created (admin/admin123)")

        # Sample Plans
        if MembershipPlan.query.count() == 0:
            plans = [
                MembershipPlan(name='Monthly Basic', description='Basic gym access for 1 month.', duration_months=1, price=50.00),
                MembershipPlan(name='Quarterly Pro', description='Pro gym access with locker for 3 months.', duration_months=3, price=140.00),
                MembershipPlan(name='Half-Yearly Elite', description='Elite access with trainers for 6 months.', duration_months=6, price=260.00),
                MembershipPlan(name='Yearly VIP', description='VIP access all inclusive for 12 months.', duration_months=12, price=500.00)
            ]
            db.session.bulk_save_objects(plans)
            print("Sample plans created")
            
        # Sample Trainers
        if Trainer.query.count() == 0:
            trainers = [
                Trainer(first_name='John', last_name='Doe', email='john@gym.com', phone='1234567890', specialization='Weightlifting', experience_years=5),
                Trainer(first_name='Jane', last_name='Smith', email='jane@gym.com', phone='0987654321', specialization='Cardio', experience_years=3)
            ]
            db.session.bulk_save_objects(trainers)
            print("Sample trainers created")

        db.session.commit()
        
        # Sample Members
        if Member.query.count() == 0:
            m1 = Member(member_id='GYM-10001', first_name='Alice', last_name='Johnson', email='alice@example.com', phone='1112223333', gender='Female', join_date=date.today() - timedelta(days=30))
            m2 = Member(member_id='GYM-10002', first_name='Bob', last_name='Williams', email='bob@example.com', phone='4445556666', gender='Male', join_date=date.today())
            db.session.add_all([m1, m2])
            db.session.commit()
            print("Sample members created")
            
            # Memberships
            plan = MembershipPlan.query.first()
            membership1 = Membership(
                member_id=m1.id,
                plan_id=plan.id,
                start_date=m1.join_date,
                end_date=m1.join_date + timedelta(days=30),
                amount_total=plan.price,
                amount_paid=plan.price
            )
            db.session.add(membership1)
            db.session.commit()
            
            # Payment
            payment = Payment(
                member_id=m1.id,
                amount=plan.price,
                payment_date=m1.join_date,
                payment_method='Credit Card',
                transaction_id='TRX-SEED-001'
            )
            db.session.add(payment)
            
            # Attendance
            att = Attendance(
                member_id=m1.id,
                date=date.today(),
                time_in=datetime.strptime('09:00', '%H:%M').time()
            )
            db.session.add(att)
            
            db.session.commit()
            print("Sample membership, payment and attendance created")

if __name__ == '__main__':
    seed_data()
