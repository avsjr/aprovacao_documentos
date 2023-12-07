from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configura o login
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@login_manager.request_loader
def load_user_from_request(request):
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    return user

# Rotas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        full_name = request.form.get("full_name")
        department = request.form.get("department")
        email = request.form.get("email")
        password = request.form.get("password")

        # Cria um novo usuário
        user = User(full_name=full_name, department=department, email=email)
        user.set_password(password)  # Hasheia a senha antes de salvar
        db.session.add(user)
        db.session.commit()

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
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)  # Adicione esta linha
    department = db.Column(db.String(120), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

# Inicia o servidor
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)