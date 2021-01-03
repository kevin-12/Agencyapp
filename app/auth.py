import os
import functools
from flask import (Blueprint,flash,g,redirect,render_template,session,request
,url_for)
from werkzeug.security import check_password_hash,generate_password_hash
from passlib.hash import pbkdf2_sha256
from .wtform_fields import *
from .db import *
import psycopg2
import postgresql
from .model import *
from werkzeug.utils import secure_filename
app = Flask(__name__,instance_relative_config=True)
UPLOAD_FOLDER = 'app/static/Profile/CV'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
bp=Blueprint('auth',__name__,url_prefix='/auth')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#setting file to allowed file
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Client registation form,membership
@bp.route('/register', methods=('GET', 'POST'))
def register():
    reg_form = RegistrationForm(request.form)
    if request.method == 'POST'and reg_form.validate():
        #Get Data
        Username= reg_form.Username.data

        password=reg_form.password.data
        email=reg_form.email.data  
        #hash password for security
        hashed_password=pbkdf2_sha256.hash(password)
        #Data query -flask-alchemy
        user_object=User.query.filter_by(Username=Username).first()
        if user_object:
           message='User Already Taken'
           return render_template('auth/register.html',form=reg_form,message=message)
        user=User(Username=Username,password=hashed_password,email=email)

        db_session.add(user)
        db_session.commit()
        return render_template('auth/login.html',form=reg_form)
    return render_template('auth/register.html',form=reg_form)
 
 #Login form
@bp.route('/login', methods=('GET', 'POST'))
def login():
    form=LoginForm(request.form)
    if request.method == 'POST' and form.validate() :
        Username=form.Username.data
        #connect to database
        #Check user from database
        user = User.query.filter_by(Username=Username).first()
        session.clear()
        session["username"] = Username
        return redirect(url_for('index'))
    return render_template('auth/login.html',form=form)
 #session
@bp.before_app_request
def load_logged_in_user():
    user_name = session.get('username')
   
    if user_name is None:
        g.user = None
    else:
        g.user = User.query.filter_by(Username=user_name).first()
 #logout 
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))   
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

 #nanny application form
@bp.route('/application', methods=('GET','POST'))
def application():
 
    applicationForm = NannyApplicationForm(request.form)

    if request.method == 'POST'and applicationForm.validate():
        Name=applicationForm.name.data
        Username= applicationForm.username.data
        password=applicationForm.password.data
        email=applicationForm.email.data  
        password=applicationForm.password.data
        city=applicationForm.city.data 
        hashed_password=pbkdf2_sha256.hash(password)
        file=request.files['file']

        user_object=Nanny.query.filter_by(Username=Username).first()
        if user_object:
            message='User name already taken,please insert a new username'

            return render_template('auth/ApplicationForm.html', applicationForm = applicationForm,message=message )
        
        #Makesure it is safe
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            cv_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(cv_path)

           #Create a path for data base
            p=os.path.split(cv_path)
           #take the last child,this help in rendering in html
            db_path= p[-1]
            db_database=db_path 
            print(db_database)

           
        new_nanny = Nanny(Name=Name,Username=Username,password=hashed_password,email=email,city=city ,curriculum=db_database)
        
        db_session.add(new_nanny)
        db_session.commit()


        nanny=Nanny.query.filter_by(Username=Username).first()

        


        return render_template('auth/Thankyou.html',nanny=nanny )
        
    return render_template('auth/ApplicationForm.html', applicationForm = applicationForm )

            