from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SelectField, DateTimeField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import datetime
from wtforms_components import IntegerField
from database import get_categories, get_countries


class MovieEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1887, max=datetime.now().year)], default=1887)
    category = SelectField('Category', choices=get_categories())
    country = SelectField('Country', choices=get_countries())
    image = FileField('Image', validators=[Optional()])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0, max=50)], default=1)
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0, max=1000)], default=1)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class CreateUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional()])
    dateBirth = DateTimeField('Date', validators=[Optional()], format='%d/%m/%Y', default=datetime(1999, 1, 1))
    role = SelectField('Role', choices=['Admin', 'Normal user'])
    image = FileField()


class CategoryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])


class CountryForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])


class PaymentCash(FlaskForm):
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])