from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Configura o login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Rotas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Cria um novo usuário
        user = User(username=username, password=password, email=email)
        user.save()

        # Faz o login do usuário
        login_user(user)

        return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Tenta fazer o login do usuário
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return render_template("login.html", error="Usuário ou senha inválidos")

        # Faz o login do usuário
        login_user(user)

        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))

# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)
