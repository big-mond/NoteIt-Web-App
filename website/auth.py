from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

#Authorization Blueprint for app
auth = Blueprint('auth', __name__)


#Login Settings
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        #If method POST, pulls info from form
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        
        #User is verified by matching email
        user = User.query.filter_by(email=email).first()
        
        if user:
            
            #If email matches check password hash
            if check_password_hash(user.password, password):
                
                #if password hash matches, log user in with success message
                flash('Logged in successfully!', category='success')
                
                #Keep user logged in
                login_user(user, remember=True)
                
                #Redirect to home page
                return redirect(url_for('views.home'))
            else:
                
                #If password incorrect, flash error message
                flash('Incorrect password, try again.', category='error')
        else:
           
            #If Email does not match, flash error message 
            flash('Email does not exist.', category='error')
    
    #Template for login page
    return render_template("login.html", user=current_user) 

#Logout Settings
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    
    #After Logout, return to Login page
    return redirect(url_for('auth.login'))

#Signup Settings
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        #If method POST, pulls info from form
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        #Query database for existing emails
        email_exists = User.query.filter_by(email=email).first()
        
        #Query database for existing usernames
        username_exists = User.query.filter_by(username=username).first()
        
        #New user checklist
        if email_exists:
            
            #If email exists, flash error message
            flash('Email is already in use.', category='error')
        elif username_exists:
            
            #If username exists, flash error message
            flash('Username already exists.', category='error')
        elif len(email) < 4:
            
            #If email length less than four characters, flash error message
            flash('Email must be greater than 3 characters.', category='error')
            pass
        elif len(username) < 2:
            
            #If username length less than two characters, flash error message
            flash('Username must be greater than 1 character.', category='error')
            pass
        elif password1 != password2:
            
            #If passwords dont match, flash error message
            flash('Passwords don\'t match.', category='error')
            pass
        elif len(password1) < 7:
            
            #If password length less than 7 characters, flash error message
            flash('Password must be at least 7 characters.', category='error')
            pass
        else:
            
            #If form clears checks, create new user
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            
            #Add new user to database
            db.session.add(new_user)
            db.session.commit()
            
            #Login user with success message
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            
            #Redirect to Home page
            return redirect(url_for('views.home'))
    
    #Template for signup page
    return render_template("signup.html", user=current_user)

