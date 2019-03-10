from add_news import AddNewsForm
from db import DB
from flask import Flask, redirect, render_template, session, request
from login_form import LoginForm
from news_model import NewsModel
from users_model import UsersModel
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()


# http://127.0.0.1:8080/login
@app.route('/SingUp', methods = ["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template('sign_up.html', title='Авторизация')
    elif request.method == "POST":
        user_model = UsersModel(db.get_connection())
        print(request.form['nicame'], request.form['name'], request.form['pass'])
        user_model.insert(request.form['nicame'], request.form['name'], request.form['pass'])
        session['username'] = request.form['name']
        session['user_id'] = request.form['nicame']
        return redirect("/index")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html', title='Авторизация')
    elif request.method == "POST":
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(request.form['nicname'], request.form['pass'])
        if (exists[0]):
            session['username'] = exists[1]
            session['user_id'] = request.form['nicname']
        return redirect("/index")
    return render_template('sign_up.html', title='Авторизация')



@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('index.html', username=session['username'], news=news)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='Добавление новости', form=form, username=session['username'])


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")



if __name__ == '__main__':
    um = NewsModel(db.get_connection())
    print(um.get_all())
    app.run(port=8080, host='127.0.0.1', debug=True)