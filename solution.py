from flask import Flask, redirect, render_template, session, request

from db import DB
from news_model import NewsModel
from users_model import UsersModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()
try:
    users_img = NewsModel(db.get_connection()).get_all()[-1][0]
except:
    users_img = 0


# http://127.0.0.1:8080/login
@app.route('/SignUp', methods=["GET", "POST"])
def sign_up():
    if request.method=="GET":
        return render_template('sign_up.html', title='Авторизация', error=None)
    elif request.method=="POST":
        user_model = UsersModel(db.get_connection())
        if not user_model.get(request.form['nikname']):
            user_model.insert(request.form['nikname'], request.form['name'], request.form['pass'])
            session['username'] = request.form['name']
            session['user_id'] = request.form['nikname']
            return redirect("/main")
        else:
            return render_template('sign_up.html', title='Авторизация', error="this nikname already exists")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect("/main")
    if request.method=="GET":
        return render_template('login.html')
    elif request.method=="POST":
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(request.form['nikname'], request.form['pass'])
        if (exists[0]):
            session['username'] = exists[1]
            session['user_id'] = request.form['nikname']
        return redirect("/main")
    return redirect("/SignUp")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' not in session:
        return redirect('/login')
    newsi = list(reversed(NewsModel(db.get_connection()).get_all()))
    news = [[i for i in a] for a in newsi]
    #if 'like' in request.form:
    #print(request.form["like"])
    for i in range(len(newsi)):
        news[i][3] = newsi[i][3].split('\n')
    return render_template('main.html', username=session['username'], session=session, news=news, like=like)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    global users_img
    if 'username' not in session:
        return redirect('/login')
    if request.method=="GET":
        return render_template('add_news.html', title='Добавление новости', username=session['username'])
    elif request.method=="POST":
        nm = NewsModel(db.get_connection())
        request.files["file"].save("static/img/users_img/{}.png".format(users_img))
        recipe = request.form["recipe"]

        nm.insert(request.form["name"], users_img, recipe, session["user_id"])
        users_img += 1
        return redirect('/')


@app.route('/user/<user_id>')
def user(user_id):
    newsi = list(reversed(NewsModel(db.get_connection()).get_all(user_id)))
    news = [[i for i in a] for a in newsi]
    for i in range(len(newsi)):
        news[i][3] = newsi[i][3].split('\n')
    username = UsersModel(db.get_connection()).get(user_id)[1]
    return render_template('user.html', username=username, session=session, news=news, like=like)


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    if nm.get(news_id)[4]==session['user_id']:
        nm.delete(news_id)
    return redirect("/main")


def like(news_id, val):
    nm = NewsModel(db.get_connection())
    nm.update_rating(news_id, val)


if __name__=='__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
