import os
from flask import Flask
from flask import (Blueprint,flash,g,redirect,render_template,request,session
,url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    if __name__ == "__main__":
    
    app.secret_key='_5#y2L"F4Q8z\n\xec]/'
    #Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bootstrap = Bootstrap(app)
    
    if test_config is None:
    # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
    # load the test config if passed in
        app.config.from_mapping(test_config)

    #  ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
   #application created
    from app.db import db_session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
   
    @app.route('/')
    def home( name=None):
       return render_template('/home2/hom.html')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import nanny
    app.register_blueprint(nanny.bp)
    app.add_url_rule('/', endpoint='index')        
    return app