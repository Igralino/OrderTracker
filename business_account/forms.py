from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextAreaField, SelectField, StringField, FieldList, PasswordField, SubmitField, DateField
from wtforms.fields.html5 import EmailField, DecimalRangeField
from wtforms.validators import DataRequired, Length, Email, NumberRange


class RegistrationBusinessForm(FlaskForm):
    name = StringField('Название бизнеса',
                       validators=[DataRequired(message="Заполните это поле"),
                                   Length(min=2, max=50,
                                          message='Это поле должно содержать от 2 до 50 символов')])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message="Заполните это поле"),
                                         Length(min=5, max=30,
                                                message='Это поле должно содержать от 5 до 30 символов')])
    check_password = PasswordField('Повторите пароль',
                                   validators=[DataRequired(message="Заполните это поле"),
                                               Length(min=5, max=30,
                                                      message='Это поле должно содержать от 5 до 30 символов')])

    email = EmailField('Почта',
                       validators=[DataRequired(message="Заполните это поле"),
                                   Length(min=5, max=50, message='Это поле должно содержать от 5 до 50 символов'),
                                   Email(message='Введите правильную почту')])


class LoginBusinessForm(FlaskForm):
    email = EmailField('Почта',
                       validators=[DataRequired(message="Заполните это поле"),
                                   Length(min=5, max=50, message='Это поле должно содержать от 5 до 50 символов'),
                                   Email(message='Введите правильную почту')])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message="Заполните это поле"),
                                         Length(min=5, max=30,
                                                message='Это поле должно содержать от 5 до 30 символов')])


class ChangeBusinessNameForm(FlaskForm):
    new_name = StringField('Новое название бизнеса',
                           validators=[DataRequired(message="Заполните это поле"),
                                       Length(min=2, max=50,
                                              message='Это поле должно содержать от 2 до 50 символов')])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message="Заполните это поле"),
                                         Length(min=5, max=30,
                                                message='Это поле должно содержать от 5 до 30 символов')])
    submit1 = SubmitField('Сохранить изменения')


class ChangeBusinessPasswordForm(FlaskForm):
    new_password = PasswordField('Новый пароль',
                                 validators=[DataRequired(message="Заполните это поле"),
                                             Length(min=5, max=30,
                                                    message='Это поле должно содержать от 5 до 30 символов')])
    check_new_password = PasswordField('Повторите новый пароль',
                                       validators=[DataRequired(message="Заполните это поле"),
                                                   Length(min=5, max=30,
                                                          message='Это поле должно содержать от 5 до 30 символов')])
    old_password = PasswordField('Старый пароль',
                                 validators=[DataRequired(message="Заполните это поле"),
                                             Length(min=5, max=30,
                                                    message='Это поле должно содержать от 5 до 30 символов')])
    submit2 = SubmitField('Сохранить изменения')


class PossibleProcessForm(FlaskForm):
    type = StringField("Тип услуги", validators=[DataRequired(message="Заполните это поле"),
                                                 Length(min=5, max=50,
                                                        message='Это поле должно содержать от 5 до 50 символов')])
    stages = FieldList(StringField(validators=[DataRequired(message="Заполните это поле"), Length(max=50)],
                                   render_kw={'placeholder': 'Этап'}),
                       min_entries=0,
                       max_entries=10)
    desc = TextAreaField("Описание услуги",
                         validators=[DataRequired(message="Заполните это поле"),
                                     Length(min=1, max=500,
                                            message='Это поле должно содержать от 1 до 500 символов')])
    price = StringField("Цена", validators=[DataRequired(message="Заполните это поле"),
                                            Length(min=3, max=50,
                                                   message='Это поле должно содержать от 3 до 50 символов')])


class ChangePossibleProcessForm(FlaskForm):
    new_type = StringField("Тип услуги", validators=[DataRequired(message="Заполните это поле"),
                                                     Length(min=5, max=50,
                                                            message='Это поле должно содержать от 5 до 50 символов')])
    desc = TextAreaField("Описание услуги",
                         validators=[DataRequired(message="Заполните это поле"),
                                     Length(min=1, max=500,
                                            message='Это поле должно содержать от 1 до 500 символов')])
    stages = FieldList(StringField(validators=[DataRequired(message="Заполните это поле"), Length(max=50)],
                                   render_kw={'placeholder': 'Этап'}),
                       min_entries=0,
                       max_entries=10)

    price = StringField("Цена", validators=[DataRequired(message="Заполните это поле"),
                                            Length(min=3, max=50,
                                                   message='Это поле должно содержать от 3 до 50 символов')])


class UnconfirmedForm(FlaskForm):
    submit = SubmitField('Отправить снова')


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Ваша почта',
                       validators=[DataRequired(message="Заполните это поле"),
                                   Length(min=5, max=50, message='Это поле должно содержать от 5 до 50 символов'),
                                   Email(message='Введите правильную почту')])


class CreateProcessForm(FlaskForm):
    client_email = EmailField('Почта клиента',
                              validators=[DataRequired(message="Заполните это поле"),
                                          Length(min=5, max=50,
                                                 message='Это поле должно содержать от 5 до 50 символов'),
                                          Email(message='Введите правильную почту')])
    description = TextAreaField("Описание услуги",
                                validators=[DataRequired(message="Заполните это поле"),
                                            Length(min=1, max=500,
                                                   message='Это поле должно содержать от 1 до 500 символов')])
    price = StringField("Цена", validators=[DataRequired(message="Заполните это поле"),
                                            Length(min=3, max=50,
                                                   message='Это поле должно содержать от 3 до 50 символов')])


class SelectFieldTypeForm(FlaskForm):
    select_type = SelectField('Тип услуги', choices=[])


class SelectFieldStageForm(FlaskForm):
    select_stage = SelectField('Этап', choices=[])


class ChangeForm(FlaskForm):
    desc = TextAreaField('Дополнительная информация',
                         validators=[DataRequired(message="Заполните это поле"),
                                     Length(min=1, max=500,
                                            message='Это поле должно содержать от 1 до 500 символов')])
    percent = DecimalRangeField('На сколько процентов заказ закончена:', validators=[NumberRange(min=0, max=100)])
    price = StringField("Цена", validators=[DataRequired(message="Заполните это поле"),
                                            Length(min=3, max=50,
                                                   message='Это поле должно содержать от 3 до 50 символов')])


class FindForm(FlaskForm):
    words = StringField('', validators=[DataRequired(message="Заполните это поле")])


class DateForm(FlaskForm):
    dt = DateField('Срок завершения', format="%m/%d/%Y", validators=[DataRequired(message="Заполните это поле")])


class CreationCardForm(FlaskForm):
    address = StringField("Ваш адрес", validators=[DataRequired(message="Заполните это поле")])
    description = TextAreaField("Описание бизнеса",
                                validators=[DataRequired(message="Заполните это поле"),
                                            Length(min=1, max=500,
                                                   message='Это поле должно содержать от 1 до 500 символов')])
    contact_information = TextAreaField("Контактная информация",
                                        validators=[DataRequired(message="Заполните это поле"),
                                                    Length(min=1, max=500,
                                                           message='Это поле должно содержать от 1 до 500 символов')])


class CommentsForm(FlaskForm):
    email = EmailField('Ваша почта',
                       validators=[DataRequired(message="Заполните это поле"),
                                   Length(min=5, max=50, message='Это поле должно содержать от 5 до 50 символов'),
                                   Email(message='Введите правильную почту')])

    name = StringField('Ваше имя', validators=[DataRequired(message="Заполните это поле"),
                                               Length(min=2, max=50,
                                                      message='Это поле должно содержать от 2 до 50 символов')])

    text = StringField('Ваш комментарий', validators=[DataRequired(message="Заполните это поле"),
                                                      Length(min=1, max=500,
                                                             message='Это поле должно содержать от 1 до 500 символов')])
    star = StringField('', validators=[DataRequired(message="Заполните это поле")])


class HelpForm(FlaskForm):
    desc = SelectField('Описание', choices=[])
    price = SelectField('Цена', choices=[])
    pic = SelectField('Картинка', choices=[])


class HelpIdForm(FlaskForm):
    id = StringField('id')


class WidgetDataForm(FlaskForm):
    type = SelectField('type', choices=[('adv', 'Реклама'), ('game', 'Игра')],
                       validators=[DataRequired(message="Выберите тип")])
    photo = FileField(validators=[DataRequired(message="Загрузите фото")])
    title = StringField(validators=[DataRequired(message="Добавьте подпись")])
    textpos = SelectField('textpos', choices=[(1, 'Над картинкой'), (2, 'Под картинкой')],
                          validators=[DataRequired(message="Выберите место")])
    pages = SelectField('pages', choices=[(1, 'Визитка'), (2, 'Страница заказа'), (3, 'На обеих страницах')],
                        validators=[DataRequired(message="Выберите страницы")])
    submit = SubmitField('Готово!')


class WidgetEraseForm(FlaskForm):
    pages = SelectField('pages',
                        choices=[(1, 'Визитка'), (2, 'Страница заказа'), (3, 'На обеих страницах'), (4, 'Удалить')])
    submit = SubmitField("Изменить виджет")
