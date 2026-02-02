# what is flask? it takes demands from person, analyses it and returns result.
# flask does this using certain communication standard. it binds html with python
from flask import render_template, redirect, request
from models import Product, User
from ai import generate_ai_characteristics, ai_recommend
import re
from flask_login import login_user, logout_user, login_required, current_user
from forms import ProductForm, LoginForm, RegisterForm
from ext import app, db
import os
import uuid
from werkzeug.utils import secure_filename


@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()

    if form.validate_on_submit():
        file = form.img.data  # this is filestorage object
        filename = None
        if file:
            filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
            file.save(os.path.join("static/uploads/products", filename))
        new_product = Product(name=form.name.data,
                              price=form.price.data,
                              img=filename)
        db.session.add(new_product)
        db.session.commit()

        return redirect('/')
    else:
        print(form.errors)  # already written text what error was

    return render_template('create_product.html', form=form)


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    form = ProductForm(obj=product)  # prefilling fields

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        file = form.img.data

        if file and file.filename:
            filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
            file.save(os.path.join(app.root_path, "static", filename))
            product.img = filename  # update only if new image uploaded

        # else: keep old image automatically

        db.session.commit()
        return redirect('/')

    return render_template('edit_product.html', form=form, product=product)


@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        return redirect('/')

    return render_template('delete_product.html', product=product)


@app.route('/registration', methods=['GET', 'POST'])
def registration(form=None):
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/')
    else:
        print(form.errors)  # already written text what error was

    return render_template('registration.html', form=form)


@app.route('/authorisation', methods=['GET', 'POST'])
def authorisation():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user != None and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
    else:
        print(form.errors)  # already written text what error was
    return render_template('authorisation.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    ai_description = generate_ai_characteristics(product)

    return render_template(
        'product.html',
        product=product,
        ai_description=ai_description
    )


@app.route('/ask_ai', methods=['GET', 'POST'])
@login_required
def ask_ai():
    answer = None
    recommendations=[]
    if request.method == 'POST':
        question = request.form['question']
        min_price = int(request.form['min_price'])
        max_price = int(request.form['max_price'])

        products = Product.query.filter(
            Product.price >= min_price,
            Product.price <= max_price
        ).all()

        ai_text = ai_recommend(products, question)


        ids = re.findall(r'ID:(\d+)', ai_text)#this filters everything by its id

        for pid in ids:
            product = Product.query.get(pid)
            if product:
                recommendations.append(product)

    return render_template(
        'ask_ai.html',
        recommendations=recommendations
    )

