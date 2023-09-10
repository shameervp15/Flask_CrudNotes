from flask import request, flash, render_template, redirect, url_for
from website.models import Note
from website import db
from flask_login import login_required, current_user

from flask import Blueprint

notes = Blueprint('notes', __name__)

@notes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    page = request.args.get('page', 1, type=int)
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc()).paginate(page=page, per_page=2)
    return render_template("home.html", notes=notes, user=current_user)


@login_required
@notes.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    note = Note.query.filter_by(id=id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted!', category='success')
        return redirect(url_for('notes.home'))
    else:
        flash('No notes found!')
        return redirect(url_for('notes.home'))