from flask import Flask, render_template, redirect, request, make_response
from forms.users import RegisterForm
# from forms.users import ...
from data import db_session
from data.users import User
from data.news import News
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return redirect('/login')





@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)




@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")








def main():
    db_session.global_init("db/blogs.db")
    app.run()


def init_db():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for i in range(10):
        user = User(name=f'user{i}', about=f'Teacher{i}')
        user.name = f'user{i}'
        user.about = f'Teacher + {i}'
        user.email = f'user{i}@mail.ru'
        db_sess.add(user)
    db_sess.commit()


def get_from_db():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id % 2 == 0).all()
    print(*user, sep='\n')


def delete_db():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 5).first()
    db_sess.delete(user)
    db_sess.commit()


def init_news_in_dv():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for i in range(20):
        user = db_sess.query(User).filter(User.id == i // 2 + 1).first()
        news = News(title=f'News{i}', content=f'Text', is_private=(i % 2), user=user)
        db_sess.add(news)
    db_sess.commit()


def get_user_news():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 3).first()
    for news in user.news:
        print(news)


if __name__ == '__main__':
    main()
    init_db()
    # get_from_db()
    delete_db()
    # get_user_news