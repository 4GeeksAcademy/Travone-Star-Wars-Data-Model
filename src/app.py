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
from models import db, User, Character, Planet, Favorite

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


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    return jsonify([person.serialize() for person in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id', type=int)

    if user_id is None:
        return jsonify({"error": "user_id parameter required"}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()

    result = []
    for fav in favorites:
        if fav.character_id:
            person = Character.query.get(fav.character_id)
            result.append({"type": "people", "id": fav.character_id,
                          "name": person.name if person else None})
        if fav.planet_id:
            planet = Planet.query.get(fav.planet_id)
            result.append({"type": "planet", "id": fav.planet_id,
                          "name": planet.name if planet else None})

    return jsonify(result), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if user_id is None:
        return jsonify({"error": "user_id required in request body"}), 400

    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    existing = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if existing:
        return jsonify({"error": "Planet already in favorites"}), 400

    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Favorite planet added successfully"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if user_id is None:
        return jsonify({"error": "user_id required in request body"}), 400

    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    existing = Favorite.query.filter_by(
        user_id=user_id, character_id=people_id).first()
    if existing:
        return jsonify({"error": "Person already in favorites"}), 400

    new_favorite = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Favorite person added successfully"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id', type=int)

    if user_id is None:
        return jsonify({"error": "user_id parameter required"}), 400

    favorite = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite planet deleted successfully"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.args.get('user_id', type=int)

    if user_id is None:
        return jsonify({"error": "user_id parameter required"}), 400

    favorite = Favorite.query.filter_by(
        user_id=user_id, character_id=people_id).first()
    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite person deleted successfully"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
