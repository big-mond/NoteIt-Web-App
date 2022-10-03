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
        
        #Pulls text from form
        text = request.form.get('text')
        
        if len(text) < 1:
            
            #If length of text less than one, flash error message
            flash('Note is too short!', category='error')
        
        elif not text:
            
            #If no text in text area, flash error message
            flash('Note cannot be empty', category='error')
        
        else:
            
            #If checks pass, add note to database with success message
            note = Note(text=text, author=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note created!', category='success')
            
            #Redirect to page that made POST request
            return redirect(request.url)
    
    #Pull notes by date in descending order
    notes = Note.query.order_by(Note.created_at.desc()).all()
    
    #Template linked to Home
    return render_template("home.html", user=current_user, notes=notes)


#Add Note Button
@views.route("/addnote", methods=['GET', 'POST'])
@login_required
def addnote():
    
    #Add Note Function
    if request.method == 'POST':
        
        #Pulls text from form
        text = request.form.get('text')
        
        #If length of text less than one, flash error message
        if len(text) < 1:
            flash('Note is too short!', category='error')
        
        #If no text in text area, flash error message
        elif not text:
            flash('Note cannot be empty', category='error')
        
        #If checks pass, add note to database with success message
        else:
            note = Note(text=text, author=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note created!', category='success')
            #Redirect to page that made POST request
            return redirect(request.url)
    
   


#MyPage
@views.route("/mypage/<username>", methods=['GET', 'POST'])
@login_required
def mypage(username):
    #Add Note Function
    if request.method == 'POST':
        
        #Pulls text from form
        text = request.form.get('text')
        
        #If length of text less than one, flash error message
        if len(text) < 1:
            flash('Note is too short!', category='error')
        
        #If no text in text area, flash error message
        elif not text:
            flash('Note cannot be empty', category='error')
        
        #If checks pass, add note to database with success message
        else:
            note = Note(text=text, author=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note created!', category='success')
            #Redirect to page that made POST request
            return redirect(request.url)
    
    #Checks user by username
    user = User.query.filter_by(username=username).first()

    #If not user, flash error message then redirect to home page
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    
    
    #Filter notes by user id and order by date in descending order
    notes = Note.query.filter_by(author=user.id).order_by(Note.created_at.desc())
    
    
    #Template linked to mypage
    return render_template("mypage.html", user=current_user, notes=notes, username=username)


#Delete button for notes
@views.route("/delete-note/<id>", methods=['GET', 'POST'])
@login_required
def delete_note(id):
    #Checks if note id is the same as user
    note = Note.query.filter_by(id=id).first()

    #If no note found, flash error message
    if not note:
        flash("Note does not exist.", category='error')
        
    #If current user is not same as note author, flash error message
    elif current_user.id != note.author:
        flash('You do not have permission to delete this note.', category='error')
    
    #Delete note from database and flash success message
    else:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted.', category='success')

    #Returns you to same place in page without refreshing after deletion
    return redirect(request.referrer)

#Search
@views.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    
    #Search function
    q = request.args.get('q')
    
    #If query length less than one character, flash error message
    if len(q) < 1:
            flash('Search can not be empty.', category='error')
            #Return to same page
            return redirect(request.referrer)
    
    #Pull notes and comments by date in descending order
    if q :
        notes = Note.query.filter(Note.text.contains(q)).order_by(Note.created_at.desc())
        username = Note.query.filter(Note.author.contains(q)).order_by(Note.created_at.desc())
        comments = Comment.query.filter(Comment.text.contains(q)).order_by(Comment.created_at.desc())
        
    
    #if q not found:
    #flash('No Results Found.', category='error')
    
    #Template for Search Results
    return render_template("search.html", user=current_user, notes=notes, comments=comments, username=username)


#Create Comment
@views.route("/create-comment/<note_id>", methods=['GET','POST'])
@login_required
def create_comment(note_id):
    
    #Pulls text from form
    text = request.form.get('text')

    #If no text flash error message
    if not text:
        flash('Comment cannot be empty.', category='error')
    
    #Pull notes from database by note id
    else:
        note = Note.query.filter_by(id=note_id)
        
        #If note found, add comment to database
        if note:
            comment = Comment(text=text, author=current_user.id, note_id=note_id)
            db.session.add(comment)
            db.session.commit()
        
        #If note not found, flash error message
        else:
            flash('Note does not exist.', category='error')

    #Return to same place in page without refreshing after commenting
    return redirect(request.referrer)

#Delete Comment
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    
    #Checks if user id is same as comment id
    comment = Comment.query.filter_by(id=comment_id).first()

    #If comment does not exist, flash error message
    if not comment:
        flash('Comment does not exist.', category='error')
    
    #If current user does not equal comment author, flash error message 
    elif current_user.id != comment.author and current_user.id != comment.note.author:
        flash('You do not have permission to delete this comment.', category='error')
    
    #If checks pass, delete comment from database
    else:
        db.session.delete(comment)
        db.session.commit()

    #Returns to same place in page without refreshing after deleting comment
    return redirect(request.referrer)
