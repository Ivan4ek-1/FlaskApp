import secrets
from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from data import db_session
from data.users import User
from data.dishes import Dishes
from forms.dishesform import DishesForm
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
db_session.global_init("db/food.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dishes).all()
    return render_template("main_page.html", dishes=dishes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.hashed_password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            email=form.email.data
        )
        user.set_password(form.hashed_password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_dish', methods=['GET', 'POST'])
@login_required
def add_dish():
    form = DishesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dishes = Dishes()
        dishes.title = form.title.data
        dishes.content = form.content.data
        dishes.created_date = form.created_date.data
        dishes.image = form.image.data
        current_user.dishes.append(dishes)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('dishes.html', title='Добавление новости',
                           form=form)


@app.route('/dishes/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dish(id):
    form = DishesForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dishes = db_sess.query(Dishes).filter(Dishes.id == id,
                                          Dishes.user == current_user).first()
        if dishes:
            form.title.data = dishes.title
            form.content.data = dishes.content
            form.created_date.data = dishes.created_date
            form.image.data = dishes.image
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dishes = db_sess.query(Dishes).filter(Dishes.id == id,
                                          Dishes.user == current_user).first()
        if dishes:
            dishes.title = form.title.data
            dishes.content = form.content.data
            dishes.created_date = form.created_date.data
            dishes.image = form.image.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('dishes.html',
                           title='Редактирование блюда', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dishes).filter(Dishes.id == id,
                                      Dishes.user == current_user).first()
    if dishes:
        db_sess.delete(dishes)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
