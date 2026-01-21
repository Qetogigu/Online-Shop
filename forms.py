from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, FileField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, length, equal_to


class ProductForm(FlaskForm):
    name=StringField('enter product name', validators=[DataRequired()])
    #z.B placeholder=form.name.label.text... from create_product.html
    price=IntegerField('enter product price', validators=[DataRequired()])
    img=FileField('enter product image', validators=[DataRequired()])

    submit = SubmitField('submit')
    edit = SubmitField('edit')
    delete = SubmitField('delete')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), length(min=8)])
    repeat_password = PasswordField('repeat password', validators=[equal_to('password')])
    sign_up = SubmitField('register')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), length(min=8)])
    sign_in = SubmitField('login')