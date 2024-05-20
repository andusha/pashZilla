from datetime import datetime, time
from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    BooleanField,
    PasswordField,
    IntegerField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    InputRequired,
    NumberRange,
)
from wtforms.fields import DateField, DateTimeField, DateTimeLocalField


class LoginForm(FlaskForm):
    email = StringField(
        render_kw={"placeholder": "Email"},
    )
    psw = PasswordField(
        "Пароль: ",
        validators=[
            DataRequired(),
            Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов"),
        ],
        render_kw={"placeholder": "Пароль"},
    )
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField(
        "ФИО: ",
        validators=[
            Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")
        ],
        render_kw={"placeholder": "ФИО"},
    )
    email = StringField(
        "Email: ",
        validators=[Email("Некорректный email")],
        render_kw={"placeholder": "Email"},
    )
    phone = StringField("Phone: ", render_kw={"placeholder": "Телефон"})
    psw = PasswordField(
        "Пароль: ",
        validators=[
            DataRequired(),
            Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов"),
        ],
        render_kw={"placeholder": "Пароль"},
    )

    submit = SubmitField("Регистрация")


class StatementForm(FlaskForm):

    problem = TextAreaField(
        "Опишите проблему",
        validators=[DataRequired(), Length(min=10, max=10000)],
        render_kw={"placeholder": "Опишите проблему"},
    )
    car = StringField(
        "Укажите марку машины", render_kw={"placeholder": "Укажите марку машины"}
    )
    date = DateTimeLocalField(
        render_kw={"placeholder": "Дата брони"},
    )

    submit = SubmitField("Оставить заявку")
