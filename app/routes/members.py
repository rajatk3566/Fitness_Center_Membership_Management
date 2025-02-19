from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Member
from datetime import datetime
from flask_login import login_required

members = Blueprint('members', __name__)

@members.route('/add', methods=['GET', 'POST'])
@login_required
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        join_date = datetime.strptime(request.form['join_date'], "%Y-%m-%d")

        try:
            new_member = Member(name=name, email=email, phone_number=phone_number, join_date=join_date)
            db.session.add(new_member)
            db.session.commit()
            flash("Member added successfully!", "success")
            return redirect(url_for('members.view_members'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding member: {e}", "danger")

    return render_template('add.html')

@members.route('/view_members')
@login_required
def view_members():
    members = Member.query.all()
    return render_template('view_member.html', members=members)


@members.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)

    if request.method == 'POST':
        member.name = request.form['name']
        member.email = request.form['email']
        member.phone_number = request.form['phone_number']
        member.join_date = datetime.strptime(request.form['join_date'], "%Y-%m-%d")
        
        try:
            db.session.commit()
            flash("Member updated successfully!", "success")
            return redirect('/view_members')
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating member: {e}", "danger")

    return render_template('edit_member.html', member=member)


@members.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    
    try:
        db.session.delete(member)
        db.session.commit()
        flash("Member deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting member: {e}", "danger")

    return redirect('/view_members')
