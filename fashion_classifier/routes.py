import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect
from fashion_classifier import app,db,bcrypt
from fashion_classifier.forms import RegistrationForm,LoginForm,Classify
from fashion_classifier.models import User,ClothingData
from flask_login import login_user,current_user,logout_user,login_required


@app.route("/home")
def home():
    return render_template("home.html")

@login_required
@app.route("/about")
def about():
    return render_template("about.html")




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/photos', picture_fn)
    ##over here I am resizing the image
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@login_required
@app.route("/classifier_page",methods=['GET','POST'])
def classifier():
    form = Classify()
    if form.validate_on_submit():
        if form.image_file.data:
            ##here we are saving the picture
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
        cloth_type = form.cloth_types.data
        gender_type = form.gender_types.data
        size_type = form.size_types.data
        color = form.color.data
        image_file = form.image_file.data

        new_clothing = ClothingData(
            cloth_type=cloth_type,
            gender_type=gender_type,
            size_type=size_type,
            color=color,
            image_file=image_file
        )
        db.session.add(new_clothing)
        db.session.commit()

    return render_template("classifier.html",form=form)


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in","success")
        return redirect(url_for('login'))
    return render_template("register.html",form=form,title='Register',hide_navbar=True)

@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Welcome User!!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful.Please check your email and password","danger")
    return render_template("login.html",form=form,title='Login',hide_navbar=True)


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


