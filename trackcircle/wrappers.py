from functools import wraps
from flask import g, request, redirect, url_for, flash

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('You must login to use this feature.')
            return redirect(url_for('general.index'))
        return f(*args, **kwargs)
    return decorated_function
    
