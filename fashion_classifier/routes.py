import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from fashion_classifier import app,db,bcrypt,mail
from fashion_classifier.forms import RegistrationForm,LoginForm,Classify,RequestResetForm,ResetPasswordForm,UpdateAccountForm
from fashion_classifier.models import User,ClothingData,TSHIRT, SHIRT, PANTS, SHORTS, JACKETS, CAPS
from flask_login import login_user,current_user,logout_user,login_required
import datetime





from werkzeug.utils import secure_filename
@app.route("/home")
def home():
    return render_template("home.html")

@login_required
@app.route("/about")
def about():
    return render_template("about.html")



# def decode_base64(value):
#     return Markup(base64.b64decode(value).decode('utf-8'))
#
# # Add the filter to the Jinja2 environment
# app.jinja_env.filters['decode_base64'] = decode_base64


@app.route("/display_images")
def display_image():
    clothing_items = ClothingData.query.all()
    User_credentials = User.query.all()


    return render_template("display_image.html", clothing_items=clothing_items,User_credentials=User_credentials)


@app.route("/data_table")
def data_table():
    clothing_items = ClothingData.query.all()

    return render_template("data_table.html", clothing_items=clothing_items)





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@login_required
@app.route("/User_account", methods=['GET', 'POST'])
def User_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('User_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename=current_user.image_file)



    return render_template("User_account.html", title='Account', image_file=image_file, form=form)


@login_required
@app.route("/User_Inventory")
def User_Inventory():
    # Get the entries for the current user
    user_id = current_user.id

    tshirt_count = TSHIRT.query.filter_by(user_id=user_id).count()
    shirt_count = SHIRT.query.filter_by(user_id=user_id).count()
    caps_count = CAPS.query.filter_by(user_id=user_id).count()
    shorts_count = SHORTS.query.filter_by(user_id=user_id).count()
    pants_count = PANTS.query.filter_by(user_id=user_id).count()
    jackets_count = JACKETS.query.filter_by(user_id=user_id).count()

    return render_template("User_Inventory.html", tshirt_count=tshirt_count, shirt_count=shirt_count,
                           caps_count=caps_count, shorts_count=shorts_count,
                           pants_count=pants_count, jackets_count=jackets_count,user_id=user_id)

@login_required
@app.route("/total_inventory")
def total_inventory():
    tshirt_count = TSHIRT.query.count()
    shirt_count = SHIRT.query.count()
    caps_count = CAPS.query.count()
    shorts_count = SHORTS.query.count()
    pants_count = PANTS.query.count()
    jackets_count = JACKETS.query.count()

    return render_template("total_inventory.html", tshirt_count=tshirt_count, shirt_count=shirt_count,
                           caps_count=caps_count, shorts_count=shorts_count,
                           pants_count=pants_count, jackets_count=jackets_count)



@login_required
@app.route("/classifier_page",methods=['GET','POST'])
def classifier():
    form = Classify()

    if form.validate_on_submit():
        cloth_type = form.cloth_types.data
        gender_type = form.gender_types.data
        size_type = form.size_types.data
        color = form.color.data
        image_file = request.files['image_file']
        user_name = form.username.data




        image_info = image_file.read()

            # Create a new ClothingData entry
        new_clothing = ClothingData(
             cloth_type=cloth_type,
             gender_type=gender_type,
             size_type=size_type,
             color=color,
             user_id=current_user.id,
             date = datetime.date.today(),
             image_data = image_info,
             user_name=user_name
            )

        db.session.add(new_clothing)
        db.session.commit()

        # Based on the cloth_type, create a new entry in the specific clothing category table
        clothing_item = None

        if cloth_type in ['TSHIRT', 'SHIRT', 'PANTS', 'SHORTS', 'JACKETS', 'CAPS']:
            if cloth_type == 'TSHIRT':
                clothing_item = TSHIRT(
                    size=size_type,
                    gender_type=gender_type,
                    color=color,
                    date=datetime.date.today(),
                    user_id=current_user.id,
                    image_data=image_info,
                    user_name=user_name



                )
            elif cloth_type == 'SHIRT':
                clothing_item = SHIRT(
                    size=size_type,
                    gender_type=gender_type,
                    color=color,
                    date=datetime.date.today(),
                    user_id=current_user.id,
                    image_data=image_info,
                    user_name=user_name



                )
            elif cloth_type == 'PANTS':
                clothing_item = PANTS(
                    size=size_type,
                    gender_type=gender_type,
                    color=color,
                    date=datetime.date.today(),
                    user_id=current_user.id,
                    image_data=image_info,
                    user_name=user_name



                )

            elif cloth_type == 'SHORTS':
                clothing_item = SHORTS(
                    size=size_type,
                    gender_type=gender_type,
                    color=color,
                    date=datetime.date.today(),
                    user_id=current_user.id,
                    image_data=image_info,
                    user_name=user_name



                )

            elif cloth_type == 'JACKETS':
                clothing_item = JACKETS(
                    size=size_type,
                    gender_type=gender_type,
                    color=color,
                    date=datetime.date.today(),
                    user_id=current_user.id,
                    image_data=image_info,
                    user_name=user_name



                )

            elif cloth_type == 'CAPS':
                clothing_item = CAPS(
                    size=size_type,
                    gender_type=gender_type,
                    color=color,
                    date=datetime.date.today(),
                    user_id=current_user.id,
                    image_data=image_info,
                    user_name=user_name


                )

        else:
            flash('Please select a valid clothing type.')

        if clothing_item:
            db.session.add(clothing_item)
            db.session.commit()

        return redirect(url_for('classifier'))
    return render_template("classifier.html",form=form)


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, date=datetime.date.today())
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


##THIS FUNCTION IS FOR SENDING THE MAIL TO USER FOR RESET PASSWORD
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)




##this route is for just requesting for resetting the password by putting your email
@app.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instruction to reset the password","info")
        return redirect(url_for("login"))
    return render_template('reset_request.html',title='Reset Password',form=form)




##this is for reseting the password with the token
@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid token or expired token","warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in","success")
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)












