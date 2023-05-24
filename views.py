from sqlalchemy.orm import query, session
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from models import db, login, User, Seing
from flask_login import current_user, login_user, login_required, logout_user
from forms import SearchForm, WebDataForm, LoginForm, RegisterForm
from search import Search
from server import Server

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SEING'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

db.init_app(app)
login.init_app(app)
login.login_view = 'login'


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/", methods=["POST", "GET"])
def seing():
    '''Searching func, that links db with front and searching'''
    search_form = SearchForm(request.form)
    if request.method == "POST":
        search = Search(search_form.query.data)
        session['toggle'] = search_form.toggle.data
        if search_form.toggle.data:
            net_results = search.web_search()
            return seing_results(query=search_form.query.data, results=net_results, form=search_form)
        else:
            local_results = search.top_fuzzed()
            return seing_results(query=search_form.query.data, results=local_results, form=search_form)
    else:
        return render_template("homePage.html", form=search_form)


@app.route("/results?<query>", methods=["POST", "GET"])
def seing_results(query, results, form):
    if request.method == "GET":
        return render_template("results.html", q=query, results=results, form=form)
    elif request.method == "POST":
        search = Search(form.query.data)
        form.toggle.data = session.get('toggle')
        if form.toggle.data:
            net_results = search.web_search()
            return render_template("results.html", q=form.query.data, results=net_results, form=form)
        else:
            local_results = search.top_fuzzed()
            return render_template("results.html", q=form.query.data, results=local_results, form=form)
    else:
        return redirect("/")


@app.route("/dbsocket", methods=["POST", "GET"])
def dbsocket():
    data_list_form = WebDataForm(request.form)
    if request.method == "GET":
        records = Seing.query.all()
        return render_template("dbsocket.html", records=records, form=data_list_form)
    elif request.method == "POST":
        server = Server(data_list_form.web_list.data)
        if data_list_form.web_type.data == 'list':
            records = server.data_list_handler()
            return render_template("dbsocket.html", records=records, form=data_list_form)
        elif data_list_form.web_type.data == 'query':
            records = server.data_query_hanlder()
            return render_template("dbsocket.html", records=records, form=data_list_form)
        else:
            return redirect("/")
    else:
        return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        email = login_form.email.data
        user = User.query.filter_by(email = email).first()
        if user is not None and user.check_password(login_form.password.data):
            session['usr'] = user.username
            login_user(user)
            return redirect(url_for('profile'))

    return render_template("login.html", form=login_form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    register_form = RegisterForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data
 
        if User.query.filter_by(email=email).first():
            return "<h1>Email already Present</h1>"
             
        user = User(email=email, username=username, password_hash=None)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("signup.html", form=register_form)


@app.route("/profile")
@login_required
def profile():
    if 'usr' in session:
        usr = session['usr']
        return f"<h1>Welcome {usr}</h1><br><h2><a href='/logout'>Logout Here</a></h2>"
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop('email', None)
    logout_user()
    flash('You have been logged out.')
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return f"<h1> Oops, you got lost!!</h1><br><h2>{error}</h2>"


@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query')
    if not query:
        return jsonify({'suggestions': []})
    search = Search(query)
    suggestions = search.fetch_suggestions()
    return jsonify(suggestions)


def run_app() -> None:
    app.run(debug=True)
