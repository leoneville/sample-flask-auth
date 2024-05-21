from flask import Flask, request, jsonify
from flask_login import LoginManager

from database import db
from models import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

# view login


@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            ...

        return {"message": "Usuário autenticado com sucesso."}, 200

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)
