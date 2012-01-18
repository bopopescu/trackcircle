import trackcircle.config
import boto
from flask import Flask, g, session, redirect, url_for
from .database import db_session

app = Flask(__name__)
app.config.from_object(config)

s3 = boto.connect_s3()
bucket = s3.create_bucket('dev.monospectra.com')  # bucket names must be unique


from trackcircle.facebook import facebook
from trackcircle.models import User
from trackcircle.views import general

MODULES = (
    general.mod,
)

for module in MODULES:
    app.register_blueprint(module)
    
@app.before_request
def before_request():
    g.user = None
    if 'oauth_token' in session:
        if 'user_id' in session:
            g.user = User.query.filter(User.id == session['user_id']).first()
            g.user.facebook_info = facebook.get('/me')
        else:
            redirect(url_for('general.logout'))

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()