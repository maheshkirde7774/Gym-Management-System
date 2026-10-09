from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

from .user import User
from .member import Member
from .plan import MembershipPlan
from .membership import Membership
from .payment import Payment
from .attendance import Attendance
from .trainer import Trainer
