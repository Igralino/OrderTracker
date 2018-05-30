from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    number = StringField('Номер заказа', validators=[DataRequired(message="Заполните это поле")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Заполните это поле")])
    submit = SubmitField("Найти")


class CheckBoxForm(FlaskForm):
    checkbox = BooleanField(validators=[])


class StatusEmailForm(FlaskForm):
    submit1 = SubmitField("Сохранить")


class FindForm(FlaskForm):
    words = StringField('', validators=[DataRequired(message="Заполните это поле")])
    submit2 = SubmitField("Найти")


class RatingForm(FlaskForm):
    submit2 = SubmitField("Оценить")
    star = StringField('', validators=[DataRequired(message="Заполните это поле")])


class ForgotPasswordForm(FlaskForm):
    number = StringField('Номер заказа', validators=[DataRequired(message="Заполните это поле")])
