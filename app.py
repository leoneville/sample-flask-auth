from flask import Flask, request, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from database import db
from models import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return {"message": "Usuário autenticado com sucesso."}, 200

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso."})


@app.route("/user", methods=["POST"])
@login_required
def create_user():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuário cadastrado com sucesso."}), 200

    return jsonify({"message": "Dados inválidos"}), 400


@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user: int):
    user = db.session.get(User, id_user)

    if user:
        return jsonify(user.to_dict())

    return jsonify({"message": "Usuário não encontrado."}), 404


@app.route("/users", methods=["GET"])
@login_required
def read_users():
    users = User.query.all()

    if users:
        response = [user.to_dict() for user in users]

        return jsonify(response)

    return jsonify({"message": "Nenhum usuário encontrado."}), 404


@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user: int):
    data = request.json
    user = db.session.get(User, id_user)

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso."})

    return jsonify({"message": "Usuário não encontrado."}), 404


@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user: int):
    user = db.session.get(User, id_user)

    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida."}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso."})

    return jsonify({"message": "Usuário não encontrado."}), 404


if __name__ == "__main__":
    app.run(debug=True)
