import os
from flask import Flask, request, session, g, redirect, url_for, \
            render_template, flash, send_from_directory, Blueprint
from trackcircle import app, bucket
from trackcircle.models import User
from trackcircle.models import Track
from trackcircle.wrappers import auth_required
from trackcircle.facebook import facebook
from werkzeug import secure_filename
from mutagen.easyid3 import EasyID3

from pprint import pprint

mod = Blueprint('general', __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['mp3'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@mod.route('/')
def index():
    me = None
    tracks = Track.query.order_by(Track.id.desc()).all()
    if g.user:
        me = g.user
    return render_template('general/index.html', me=me, tracks=tracks)

@mod.route('/login', methods=['GET', 'POST'])
def login():
    return facebook.authorize(callback=url_for('general.authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))
    
    
@mod.route('/authorized')
@facebook.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    if 'oauth_token' in session and me.data['id']:
        user = User.query.filter(User.facebook_id == me.data['id']).first()
        if not user:
            user = User(me.data['id'])
            user.create()
        session['user_id'] = user.id
        user.facebook_update(facebook)
        user.save()
    else:
        return 'Shit. oauth token dead or facebook.me didnt work'
    flash('You\'ve logged in!')
    return redirect(url_for('general.index'))


            
@mod.route('/upload', methods=['GET','POST'])
@auth_required
def upload():
    if request.method == 'POST':
        file = request.files['uploaded_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            saved_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_filename)
            
            
            track = Track(g.user.id, filename)
            if bucket.get_key(track.keyname):
                flash('Song already exists on server')
                return redirect(url_for('general.upload'))
                
            key = bucket.new_key(track.keyname)
            key.set_contents_from_filename(saved_filename)
            key.set_acl('public-read')
            
            tags = EasyID3(saved_filename)
            if tags:
                track.artist = tags['artist'][0]
                track.title = tags['title'][0]
                
            track.create()
            os.unlink(saved_filename)
            flash('Uploaded new song "%s"' % track.keyname)            
            return redirect(url_for('general.index'))     
        else:
            flash('There was an error. Either no file or file not allowed')        
        return redirect(url_for('general.upload'))        
    return render_template('general/upload.html', me=g.user)

@mod.route('/logout')
@auth_required
def logout():
    session.pop('user_id', None)
    session.pop('oauth_token', None)
    g.user = None
    flash('You were logged out.')
    return redirect(url_for('.index'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
    
@mod.before_request
def before_request():
    g.user = None
    if 'oauth_token' in session:
        if 'user_id' in session:
            g.user = User.query.filter(User.id == session['user_id']).first()
        else:
            redirect(url_for('general.logout'))

@mod.route('/crossdomain.xml')
def crossdomain():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'crossdomain.xml')
    
@mod.route('/img/<name>.<ext>')
def img(name, ext):
    mimetype = "image/png"
    if ext == "jpg" or ext == "jpeg":
        mimetype = "image/jpeg"
    elif ext == "gif":
        mimetype = "image/gif"
    
    return send_from_directory(os.path.join(app.root_path, 'img'),
            name + '.' + ext, mimetype=mimetype)
