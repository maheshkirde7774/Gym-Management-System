from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.trainer import Trainer

trainers_bp = Blueprint('trainers', __name__)

@trainers_bp.route('/')
@login_required
def list_trainers():
    trainers = Trainer.query.all()
    return render_template('admin/trainers.html', trainers=trainers)

@trainers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_trainer():
    if request.method == 'POST':
        trainer = Trainer(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            specialization=request.form.get('specialization'),
            experience_years=request.form.get('experience_years'),
            is_active=True if request.form.get('is_active') == 'on' else False
        )
        db.session.add(trainer)
        db.session.commit()
        flash('Trainer added successfully!', 'success')
        return redirect(url_for('trainers.list_trainers'))
        
    return render_template('admin/trainer_form.html', trainer=None)

@trainers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_trainer(id):
    trainer = Trainer.query.get_or_404(id)
    
    if request.method == 'POST':
        trainer.first_name = request.form.get('first_name')
        trainer.last_name = request.form.get('last_name')
        trainer.email = request.form.get('email')
        trainer.phone = request.form.get('phone')
        trainer.specialization = request.form.get('specialization')
        trainer.experience_years = request.form.get('experience_years')
        trainer.is_active = True if request.form.get('is_active') == 'on' else False
        
        db.session.commit()
        flash('Trainer updated successfully!', 'success')
        return redirect(url_for('trainers.list_trainers'))
        
    return render_template('admin/trainer_form.html', trainer=trainer)
