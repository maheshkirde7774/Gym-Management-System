from flask import Blueprint, render_template
from models.plan import MembershipPlan
from models.trainer import Trainer

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    trainers = Trainer.query.filter_by(is_active=True).limit(3).all()
    return render_template('home.html', plans=plans, trainers=trainers)

@public_bp.route('/about')
def about():
    return render_template('about.html')

@public_bp.route('/membership')
def membership():
    plans = MembershipPlan.query.filter_by(is_active=True).all()
    return render_template('membership.html', plans=plans)

@public_bp.route('/trainers')
def trainers():
    trainers_list = Trainer.query.filter_by(is_active=True).all()
    return render_template('trainers.html', trainers=trainers_list)

@public_bp.route('/services')
def services():
    return render_template('services.html')

@public_bp.route('/contact')
def contact():
    return render_template('contact.html')
