# main.py
from django.contrib.auth.models import User
import hashlib
import flask


user = User.objects.get(username='johndoe')
hashed_password = user.password

app = flask.Flask(__name__)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if password.eq(hashed_password):
        return flask.redirect(flask.url_for('dashboard'))
    else:
        return flask.render_template('login.html', error='Invalid Credentials')
    
    

def hash_string(text):
    hash_object = hashlib.sha256(text.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


