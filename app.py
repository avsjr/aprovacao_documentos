from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random
import string
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = "your-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
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
@login_required
def index():
    # Lógica para a área do usuário
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

        # Envie um e-mail para o usuário
        send_registration_email(user.email)

        # Exibe uma mensagem de sucesso
        flash("Cadastro realizado com sucesso! Um e-mail foi enviado para confirmação.", "success")

        # Redireciona para a página inicial
        return redirect(url_for("index"))
    
def send_registration_email(email):
    subject = "Cadastro realizado com sucesso!"
    body = "Obrigado por se cadastrar no nosso aplicativo. Seu cadastro foi realizado com sucesso!"
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        # Tenta fazer o login do usuário
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            error_message = "Usuário ou senha inválidos"
            return render_template("login.html", error=error_message)

        # Faz o login do usuário
        login_user(user)

        return redirect(url_for("user"))

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("reset_password.html")
    elif request.method == "POST":
        email = request.form.get("email")

        # Verifica se o e-mail está associado a uma conta existente
        user = User.query.filter_by(email=email).first()
        if user:
            # Gera um token de redefinição de senha
            reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            
            # Salva o token no banco de dados
            user.reset_password_token = reset_token
            db.session.commit()

            # Envia um e-mail ao usuário com o link de redefinição de senha
            send_reset_password_email(user.email, reset_token)

            flash("Um email com instruções para redefinir sua senha foi enviado.")
        else:
            flash("Este endereço de e-mail não está associado a uma conta.")

        return redirect(url_for("login"))

def send_reset_password_email(email, token):
    msg = Message("Redefinir Senha", sender="ti@platinacsc.com.br", recipients=[email])
    msg.body = f"Para redefinir sua senha, clique no link a seguir: {url_for('reset_password_confirm', token=token, _external=True)}"
    mail.send(msg)

@app.route("/reset_password_confirm/<token>", methods=["GET", "POST"])
def reset_password_confirm(token):
    user = User.query.filter_by(reset_password_token=token).first()

    if user is None:
        flash("Token inválido ou expirado.")
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("reset_password_confirm.html", token=token)
    elif request.method == "POST":
        password = request.form.get("password")

        # Atualiza a senha e limpa o token de redefinição
        user.set_password(password)
        user.reset_password_token = None
        db.session.commit()

        flash("Senha redefinida com sucesso. Faça login com a nova senha.")
        return redirect(url_for("login"))

@app.route("/user")
@login_required
def user():
    # Lógica para a área do usuário
    return render_template("user.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

# Modelos
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)  # Adicione esta linha
    department = db.Column(db.String(120), nullable=True)
    reset_password_token = db.Column(db.String(32), nullable=True)
    reset_password_token = db.Column(db.String(100), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self):
        self.reset_password_token = secrets.token_urlsafe(20)
        self.reset_password_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

    def check_reset_token_validity(self):
        return self.reset_password_token_expires > datetime.utcnow()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

# Inicia o servidor
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)