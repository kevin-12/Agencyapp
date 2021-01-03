import postgresql
import sqlalchemy as DB
import os
from sqlalchemy import update
from PIL import Image 
from flask import (
Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy.orm import scoped_session, sessionmaker 
from werkzeug.exceptions import abort
from app.auth import login_required
from .model import *
from .db import *
from .wtform_fields import *
from werkzeug.utils import secure_filename

#format the upload file into required path
UPLOAD_FOLDER = 'app/static/Profile/CV'
app = Flask(__name__,instance_relative_config=True)
bp = Blueprint('nanny', __name__)
Session=sessionmaker(bind=engine)
s=Session()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#bookin form
@bp.route('/book', methods=('POST','GET'))
def book():

    if request.method == 'POST'  :
        city=request.form['city']
        nanny=Nanny.query.filter_by(city=city).all()
       
        if nanny :
            return render_template('nann/search.html',nannies=nanny)
        else:
            message="we are sorry we don't have in this City "
            return render_template('nann/book.html',form=form,message=message)
    return render_template('nann/book.html',form=form)


#View profile of selected nanny
@bp.route('/<string:Username>/view_profile',methods=('POST','GET'))
def view_profile(Username):
    nanny_pictures=Nanny.query.filter_by(Username=Username).all()
    return render_template('nann/view_profile.html',nanny_pictures=nanny_pictures)

#Save booked profile into db
@bp.route('/<string:Username>/thank_you_add_to_db',methods=('POST','GET'))
def thank_you_add_to_db(Username):

    bkd_nanny=Nanny.query.filter_by(Username=Username).all()
    
    for nan in bkd_nanny:
        Name=nan.Name
        email=nan.email
        city=nan.city

        new_bkd_nanny = BookedNanny(Name=Name,Username=Username,email=email,city=city)
        db_session.add(new_bkd_nanny)
        db_session.commit()
        
    flash('Thank you for booking' +" "+  nan.Name)
    return redirect(url_for('index'))

#This is for admin-update existing profile
@bp.route('/update', methods=('POST','GET'))
def update():

    form=Book(request.form)
    if request.method == 'POST' and form.validate():
        city=form.city.data
        nanny=Nanny.query.filter_by(city=city).all()
        if nanny: 
            return render_template('nann/view.html', nannies=nanny)
        else:
            return render_template('nann/update.html',form=form)
    return render_template('nann/update.html',form=form)
@bp.route('/<userid>/upload', methods=('GET','POST'))
def upload(userid):
    if request.method =='POST':
        summary=request.form['summary']
        if 'file' not in request.files:
            flash ('files not found')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #Makesure it is safe
            filename = secure_filename(file.filename)
            photo_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(photo_path)
    
            #Create a path for data base
            p=os.path.split(photo_path)
            #take the last child,this help in rendering in html
            db_path= p[-1]
            db_database=db_path
            #Connect to the database
            nannies=Nanny.query.filter_by(id=userid).all()
            for i in nannies:
                stmt = Nanny.query.get(i.id)
                stmt.profile_picture=db_database
                stmt.summary=summary   
                db_session.commit()
            
            return  render_template('nann/uploadedth.html')
        else:
            return render_template('nann/upload.html')
    return render_template('nann/upload.html')

    #for nanny -to complete profile
@bp.route('/<userid>/complete', methods=('GET','POST'))
def complete(userid):
    if request.method =='POST':
        summary=request.form['summary']
        if 'file' not in request.files:
            flash ('files not found') 
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':

            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            photo_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(photo_path)
            #Create a path for data base
            p=os.path.split(photo_path)
            db_path= p[-1]
            db_database=db_path
            nannies=Nanny.query.filter_by(id=userid).all()
            for i in nannies:
                stmt = Nanny.query.get(i.id)
                stmt.profile_picture=db_database
                stmt.summary=summary   
                db_session.commit()
            return  render_template('nann/profilecompleted.html')  
        else:
            return render_template('nann/complete_profile.html')
    return render_template('nann/complete_profile.html')
    
    






 
    


    
