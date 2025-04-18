from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired


class DishesForm(FlaskForm):
    title = StringField('Название блюда', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    image = FileField('Изображение блюда', validators=[DataRequired()])
    created_date = DateField('Дата добавления')
    submit = SubmitField('Применить')