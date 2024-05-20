import sqlite3
import os
from flask import (
    Flask,
    render_template,
    request,
    g,
    flash,
    abort,
    redirect,
    url_for,
    make_response,
)
from wtforms import DateField, SelectField, SubmitField
from fix.FDataBase import FDataBase
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from fix.UserLogin import UserLogin
from fix.forms import LoginForm, RegisterForm, StatementForm
from werkzeug.datastructures import MultiDict

# конфигурация
DATABASE = "/tmp/v5.db"
DEBUG = True
SECRET_KEY = "fdgfh78@#5?>gfhf89dx,v06k"
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "v5.db")))

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Авторизуйтесь для доступа в личный кабинет"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource("sq_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/add/statement", methods=["POST", "GET"])
@login_required
def add_statement():
    form = StatementForm()
    if form.validate_on_submit():
        dbase.addStatement(
            current_user.get_id(), 1, form.car.data, form.problem.data, form.date.data
        )
    return render_template(
        "add_statement.html",
        title="Добавление статьи",
        form=form,
        is_auth=current_user.is_authenticated,
    )


@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    user = dbase.getUserByEmail(form.email.data)
    if current_user.is_authenticated and user["id_role"] == 1:
        return redirect(url_for("user_statements"))
    elif current_user.is_authenticated and user["id_role"] == 2:
        return redirect(url_for("admin_statements"))

    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and user["password"] == form.psw.data:
            userlogin = UserLogin().create(user)
            login_user(userlogin, remember=False)
            if user["id_role"] == 1:
                return redirect(url_for("user_statements"))
            return redirect(url_for("admin_statements"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.email.data)
        res = dbase.addUser(
            form.name.data,
            form.email.data,
            form.psw.data,
            form.phone.data,
        )
        print(res)
        if res[0]:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for("login"))
        else:
            flash(res[1], "error")

    return render_template(
        "register.html",
        title="Регистрация",
        form=form,
        is_auth=current_user.is_authenticated,
    )


@app.route("/statements")
@login_required
def user_statements():
    is_admin = dbase.getUserRole(current_user.get_id())
    user_statements = dbase.getUserStatements(current_user.get_id())
    return render_template(
        "profile.html",
        title="Профиль",
        is_auth=current_user.is_authenticated,
        is_admin=is_admin["id_role"],
        statements=user_statements,
    )


@app.route("/admin_panel", methods=["POST", "GET"])
@login_required
def admin_statements():
    is_admin = dbase.getUserRole(current_user.get_id())
    if is_admin["id_role"] != 2:
        abort(403)
    if request.method == "GET":
        user_statements = dbase.getAllStatements()
    if request.method == "POST":
        json_data = request.get_json()
        dbase.updateApprove(json_data["id"], json_data["approve"])
        return {"response": "данные отправленны коректно"}
    return render_template(
        "admin_statements.html",
        title="Все заявления",
        is_auth=current_user.is_authenticated,
        statements=user_statements,
    )


if __name__ == "__main__":
    app.run(debug=True)
