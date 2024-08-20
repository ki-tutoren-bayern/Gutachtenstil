from flask import request, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from .models import User 

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Überprüfe die Benutzerdaten in der Datenbank
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
    
    return render_template('login.html')

@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))