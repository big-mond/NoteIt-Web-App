from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Comment
from . import db

views = Blueprint('views', __name__)


@views.route("/", methods=['GET', 'POST'])
@views.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('text')
        
        if len(text) < 1:
            flash('Note is too short!', category='error')
        elif not text:
            flash('Note cannot be empty', category='error')
        else:
            note = Note(text=text, author=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note created!', category='success')
            return redirect(request.url)
    
    notes = Note.query.all()
    return render_template("home.html", user=current_user, notes=notes)

@views.route("/addnote", methods=['GET', 'POST'])
@login_required
def addnote():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Note cannot be empty', category='error')
        else:
            note = Note(text=text, author=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note created!', category='success')
            return redirect(request.url)
    
    return redirect(request.url, user=current_user)

#Username link on note
@views.route("/mypage/<username>", methods=['GET', 'POST'])
@login_required
def mypage(username):
    if request.method == 'POST':
        text = request.form.get('text')
        
        if len(text) < 1:
            flash('Note is too short!', category='error')
        elif not text:
            flash('Note cannot be empty', category='error')
        else:
            note = Note(text=text, author=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note created!', category='success')
            return redirect(request.url)
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    notes = Note.query.filter_by(author=user.id).all()
    return render_template("mypage.html", user=current_user, notes=notes, username=username)

#Delete button for notes
@views.route("/delete-note/<id>", methods=['GET', 'POST'])
@login_required
def delete_note(id):
    note = Note.query.filter_by(id=id).first()

    if not note:
        flash("Note does not exist.", category='error')
    elif current_user.id != note.author:
        flash('You do not have permission to delete this note.', category='error')
    else:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted.', category='success')

    return redirect(request.referrer)

#Search
@views.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    q = request.args.get('q')
    
    if len(q) < 1:
            flash('Search can not be empty.', category='error')
            return redirect(request.referrer)
    if q:
        notes = Note.query.filter(Note.text.contains(q))
        comments = Comment.query.filter(Comment.text.contains(q))
    
    return render_template("search.html", user=current_user, notes=notes, comments=comments)


@views.route("/create-comment/<note_id>", methods=['GET','POST'])
@login_required
def create_comment(note_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        note = Note.query.filter_by(id=note_id)
        if note:
            comment = Comment(text=text, author=current_user.id, note_id=note_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Note does not exist.', category='error')

    return redirect(request.referrer)


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.note.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(request.referrer)
