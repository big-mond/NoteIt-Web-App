from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Comment
from . import db

views = Blueprint('views', __name__)


#Home
@views.route("/", methods=['GET', 'POST'])
@views.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    
    #Add Note Function
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
    
    #Pull notes by date in descending order
    notes = Note.query.order_by(Note.date_created.desc()).all()
    
    #Template linked to Home
    return render_template("home.html", user=current_user, notes=notes)


#Add Note Button
@views.route("/addnote", methods=['GET', 'POST'])
@login_required
def addnote():
    
    #Add Note Function
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


#MyPage
@views.route("/mypage/<username>", methods=['GET', 'POST'])
@login_required
def mypage(username):
    
    #Add Note Function
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
    
    #Checks user by username
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    #Pull notes by date in descending order
    notes = Note.query.order_by(Note.date_created.desc()).all()
    
    #Pull notes by user id
    notes = Note.query.filter_by(author=user.id).all()
    
    #Template linked to mypage
    return render_template("mypage.html", user=current_user, notes=notes, username=username)


#Delete button for notes
@views.route("/delete-note/<id>", methods=['GET', 'POST'])
@login_required
def delete_note(id):
    
    #Checks if note id is the same as user
    note = Note.query.filter_by(id=id).first()

    if not note:
        flash("Note does not exist.", category='error')
    elif current_user.id != note.author:
        flash('You do not have permission to delete this note.', category='error')
    else:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted.', category='success')

    #Returns you to same page after delete
    return redirect(request.referrer)

#Search
@views.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    
    #Search function
    q = request.args.get('q')
    
    if len(q) < 1:
            flash('Search can not be empty.', category='error')
            return redirect(request.referrer)
    if q:
        #Pull notes by date in descending order
        notes = Note.query.order_by(Note.date_created.desc()).all()
        notes = Note.query.filter(Note.text.contains(q))
    
    if q:
        comments = Comment.query.order_by(Comment.date_created.desc()).all()
        comments = Comment.query.filter(Comment.text.contains(q))
    
    
    #Template for Search Results
    return render_template("search.html", user=current_user, notes=notes, comments=comments)


#Create Comment
@views.route("/create-comment/<note_id>", methods=['GET','POST'])
@login_required
def create_comment(note_id):
    
    #Pulls text from form
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        #Pull notes by note id
        note = Note.query.filter_by(id=note_id)
        
        if note:
            #Add comment to note
            comment = Comment(text=text, author=current_user.id, note_id=note_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Note does not exist.', category='error')

    #Return to same page after commenting
    return redirect(request.referrer)

#Delete Comment
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    
    #Checks if user id is same as comment id
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.note.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    #Returns to same page after deleting comment
    return redirect(request.referrer)
