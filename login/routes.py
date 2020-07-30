from flask import render_template, request, redirect, url_for, flash
from login import app, db, bcrypt
from login.models import User
from login.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from email.mime.text import MIMEText
import smtplib
import ssl



def mail_information(username, email, password):
    gmail_account = 'fpaico92@gmail.com'
    gmail_password = 'Kio000kio2'
    mail_to = email
    subject = 'Thank you for your registration.'
    html = f'''\
    <html>
        <head></head>
        <body>
            <p>kakkouです．アカウントを登録して頂きありがとうございます．
            <p>{username}さんのパスワードは{password}です．</p>
            <br />
            <br />
        </body>
    </html>
    '''
    msg = MIMEText(html, 'html')
    msg['Subject'] = subject
    msg['To'] = mail_to
    msg['From'] = gmail_account
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    send_to_list = mail_to.split(',')
    server.send_message(msg, gmail_account, send_to_list)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        mail_information(username=form.username.data, email=form.email.data, password=form.password.data)
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/secret')
@login_required
def secret():
    record = User.query.all()
    return render_template('secret.html', title='Secret', data=record)












    
