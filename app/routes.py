import os
import secrets
from flask import Flask, render_template, url_for,flash,redirect, request
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.model import Gamer,Post
from app.forms import RegisterForm,LoginForm, UpdateForm, PostForm
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home")
def home():
    game_blogs = Post.query.all()
    return render_template('Home.html',blogs = game_blogs)

@app.route('/about')
def about():
    return render_template('About.html',title = 'About')

@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            form.validate_gamer(form.gamertag)
        
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            gamer = Gamer(gamertag=form.gamertag.data, password = hashed_pwd)
            db.session.add(gamer)
            db.session.commit()
            flash(f'Account successfully created! You can now login.','success')
            return redirect(url_for('login'))
        except ValidationError as e:
            form.gamertag.errors.append(str(e))
    return render_template('Register.html',title = 'Register', form = form) #we passed the form object here

@app.route('/', methods = ['GET','POST'])
@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        gamer = Gamer.query.filter_by(gamertag = form.gamertag.data).first()
        if gamer and bcrypt.check_password_hash(gamer.password, form.password.data):
            login_user(gamer,remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else :
            flash(f'Login unsuccessful','danger')
    return render_template('Login.html',title = 'Login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_pic, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static', folder, pic_fn)
    form_pic.save(pic_path)
    return os.path.join(folder, pic_fn)  # Return the relative path


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data, folder='dps')
            current_user.image = pic_file
        try:
            form.validate_gamer(form.gamertag)
            current_user.gamertag = form.gamertag.data
            db.session.commit()
            flash('Gamer Info updated to the server!', 'success')
            return redirect(url_for('account'))
        except ValidationError as e:
            form.gamertag.errors.append(str(e))
    elif request.method == 'GET':
        form.gamertag.data = current_user.gamertag
    image = url_for('static', filename='dps/' + current_user.image)
    return render_template('Account.html', title="Account", image=image, form=form)



@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data, folder='Posts')
            image = url_for('static', filename='Posts/' + pic_file)
        else:
            image = None
        post = Post(title=form.title.data, content=form.content.data, image=image, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('home'))
    return render_template('Create.html', title='New Updates!', form=form)


