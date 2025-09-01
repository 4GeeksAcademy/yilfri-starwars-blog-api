"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite_Planet, Favorite_Character
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def getPeople():
    all_people = Character.query.all()
    results = list(map(lambda people: people.serialize(), all_people))

    return jsonify(results), 200


@app.route('/people/<int:id>', methods=['GET'])
def getSinglePeople(id):
    people = db.session.get(Character, id)
    if people is None:
        return jsonify({"error": "People not found"}), 404

    return jsonify(people.serialize()), 200


@app.route('/planets', methods=['GET'])
def getPlanets():
    planets = Planet.query.all()
    results = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(results), 200


@app.route('/planets/<int:id>', methods=['GET'])
def getPlanet(id):
    planet = db.session.get(Planet, id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    results = list(map(lambda user: user.serialize(), users))

    return jsonify(results), 200


@app.route('/users/<int:id>', methods=['GET'])
def getUser(id):
    user = db.session.get(User, id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.serialize()), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = db.session.get(User, 1)

    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    response_body = {
        "id": user.id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "favorite_planets": [
            favorite.planet.serialize() for favorite in user.favorite_planets
        ],
        "favorite_characters": [
            favorite.character.serialize() for favorite in user.favorite_characters
        ],
    }

    return jsonify(response_body), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    body = request.get_json()

    user_id = body.get("user_id")
    if not user_id:
        return jsonify({"msg": "Debes enviar un user_id"}), 400

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 400

    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 400

    favorite_exists = Favorite_Planet.query.filter_by(
        user_id=user_id, planet_id=planet_id
    ).first()
    if favorite_exists:
        return jsonify({"msg": "Ya marcaste este planeta como favorito. Selecciona otro."}), 400

    new_favorite = Favorite_Planet(user_id=user_id, planet_id=planet_id)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    body = request.get_json()

    user_id = body.get("user_id")
    if not user_id:
        return jsonify({"msg": "Debes enviar un user_id"}), 400

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 400

    character = db.session.get(Character, people_id)
    if character is None:
        return jsonify({"msg": "Personaje no encontrado"}), 400

    favorite_exists = Favorite_Character.query.filter_by(
        user_id=user_id, character_id=people_id
    ).first()
    if favorite_exists:
        return jsonify({"msg": "Ya marcaste este personaje como favorito. Selecciona otro."}), 400

    new_favorite = Favorite_Character(user_id=user_id, character_id=people_id)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    body = request.get_json()

    user_id = body.get("user_id")
    if not user_id:
        return jsonify({"msg": "Debes enviar un user_id"}), 400

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 400

    favorite = Favorite_Planet.query.filter_by(
        user_id=user_id,
        planet_id=planet_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "El planeta seleccionado no es un favorito."}), 400

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado de favoritos exitosamente"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    body = request.get_json()

    user_id = body.get("user_id")
    if not user_id:
        return jsonify({"msg": "Debes enviar un user_id"}), 400

    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 400

    favorite = Favorite_Character.query.filter_by(
        user_id=user_id,
        character_id=people_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "El personaje seleccionado no es un favorito."}), 400

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje eliminado de favoritos exitosamente"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
