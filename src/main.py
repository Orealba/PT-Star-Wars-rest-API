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
from models import db, User, People, Planets, Fav_people, Fav_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/user', methods=['GET'])
def get_user():
    allUser = User.query.all() #retorna un arreglo de clases 
    allUser = list(map(lambda elemento: elemento.serialize(), allUser))

    return jsonify(allUser), 200

@app.route('/user/favorite', methods=['GET'])
def get_user_favorite():
    allUserFavorite = Fav_people.query.all() #retorna un arreglo de clases 
    allUserFavorite = list(map(lambda elemento: elemento.serialize(), allUserFavorite))

    return jsonify(allUserFavorite), 200

@app.route('/people', methods=['GET'])
def get_people():
    allpeople = People.query.all() #retorna un arreglo de clases 
    allpeople = list(map(lambda elemento: elemento.serialize(), allpeople)) #itero en cada una de las clases y almaceno el resultado de la funcion serialize
    
    return jsonify({"resultado": allpeople})


@app.route('/planets', methods=['GET'])
def get_planets():
    allplanets = Planets.query.all() #retorna un arreglo de clases 
    allplanets = list(map(lambda elemento: elemento.serialize(), allplanets)) #itero en cada una de las clases y almaceno el resultado de la funcion serialize
    print(allplanets)
    return jsonify({"resultado": allplanets})

@app.route('/people/<int:id>', methods=['GET'])
def get_one_people(id):
    onepeople = People.query.get(id)
    if onepeople:
        onepeople = onepeople.serialize()
        return jsonify({"resultado": onepeople})
    else:
        return jsonify({"resultado": "personaje no existe"})

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    oneplanet = Planets.query.get(id)
    if oneplanet:
        oneplanet = oneplanet.serialize()
        return jsonify({"resultado": oneplanet})
    else:
        return jsonify({"resultado": "planeta no existe"})       
        
@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def add_fav_people(people_id):
    print("mensaje")
    onepeople = People.query.get(people_id)
    if onepeople:
        new = Fav_people()
        new.user_id = 1
        new.people_id = people_id
        db.session.add(new) 
        db.session.commit() 

        return jsonify({"mensaje": "Todo salio bien"})
    else:
        return jsonify({"resultado": "personaje no existe"})

@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def add_fav_planet(planet_id):
    oneplanet = Planet.query.get(planet_id)
    if oneplanet:
        new = Fav_planet()
        new.user_id = 1
        new.planet_id = planet_id
        db.session.add(new) #agrego el registro a la base de datos
        db.session.commit() #guardar los cambios realizados

        return jsonify({"mensaje": "Todo salio bien"})
    else:
        return jsonify({"resultado": "personaje no existe"})

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_one_Fav_people(id):

    Fav_people_delete = Fav_people.query.get(id)
    db.session.delete(Fav_people_delete)
    db.session.commit()
    return jsonify({"mensaje": "Todo salio bien"}),200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
