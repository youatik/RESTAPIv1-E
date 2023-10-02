from flask import jsonify
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
from bson.objectid import ObjectId

import connexion

connexion_app = connexion.App(__name__, specification_dir='./')  # Assuming api.yml is in the current directory

app = connexion_app.app

app.config["MONGO_URI"] = "mongodb://localhost:27017/A15"
mongo = PyMongo(app)


# Now, define your routes and functions

@app.route('/v1/employes', methods=['GET'])
def get_employes():
    employes = mongo.db.employes.find()
    result = []
    for employe in employes:
        employe['_id'] = str(employe['_id'])
        result.append(employe)
    return jsonify(result)

@app.route('/v1/employes', methods=['POST'])
def add_employe():
    employe = request.json
    result = mongo.db.employes.insert_one(employe)
    return jsonify({"_id": str(result.inserted_id)})

@app.route('/v1/employes/numero/<numero>', methods=['GET'])
def get_single_employe_by_numero(numero):
    employe = mongo.db.employes.find_one({'numero': numero})
    if not employe:
        return jsonify({"error": "Employe not found"}), 404
    employe['_id'] = str(employe['_id'])
    return jsonify(employe)

@app.route('/v1/employes/numero/<numero>', methods=['PUT'])
def update_employe_by_numero(numero):
    employe_data = request.json
    mongo.db.employes.update_one({'numero': numero}, {"$set": employe_data})
    return jsonify({"status": "Updated successfully"})

@app.route('/v1/employes/numero/<numero>', methods=['DELETE'])
def delete_employe_by_numero(numero):
    mongo.db.employes.delete_one({'numero': numero})
    return jsonify({"status": "Deleted successfully"})


@app.route('/v1/projets', methods=['GET'])
def get_projets():
    projets = mongo.db.projets.find()
    result = []
    for projet in projets:
        projet['_id'] = str(projet['_id'])
        result.append(projet)
    return jsonify(result)

@app.route('/v1/projets', methods=['POST'])
def add_projet():
    projet = request.json
    result = mongo.db.projets.insert_one(projet)
    return jsonify({"_id": str(result.inserted_id)})

@app.route('/v1/projets/code/<code>', methods=['GET'])
def get_single_projet_by_code(code):
    projet = mongo.db.projets.find_one({'code': code})
    if not projet:
        return jsonify({"error": "Projet not found"}), 404
    projet['_id'] = str(projet['_id'])
    return jsonify(projet)

@app.route('/v1/projets/code/<code>', methods=['PUT'])
def update_projet_by_code(code):
    projet_data = request.json
    mongo.db.projets.update_one({'code': code}, {"$set": projet_data})
    return jsonify({"status": "Updated successfully"})

@app.route('/v1/projets/code/<code>', methods=['DELETE'])
def delete_projet_by_code(code):
    mongo.db.projets.delete_one({'code': code})
    return jsonify({"status": "Deleted successfully"})

@app.route('/v1/demandes', methods=['GET'])
def get_demandes():
    demandes = mongo.db.demandes.find()
    result = []
    for demande in demandes:
        demande['_id'] = str(demande['_id'])
        result.append(demande)
    return jsonify(result)

@app.route('/v1/demandes', methods=['POST'])
def add_demande():
    demande = request.json
    result = mongo.db.demandes.insert_one(demande)
    return jsonify({"_id": str(result.inserted_id)})

@app.route('/v1/demandes/nom/<nom>', methods=['GET'])
def get_single_demande_by_nom(nom):
    demande = mongo.db.demandes.find_one({'nom': nom})
    if not demande:
        return jsonify({"error": "Demande not found"}), 404
    demande['_id'] = str(demande['_id'])
    return jsonify(demande)

@app.route('/v1/demandes/nom/<nom>', methods=['PUT'])
def update_demande_by_nom(nom):
    demande_data = request.json
    mongo.db.demandes.update_one({'nom': nom}, {"$set": demande_data})
    return jsonify({"status": "Updated successfully"})

@app.route('/v1/demandes/nom/<nom>', methods=['DELETE'])
def delete_demande_by_nom(nom):
    mongo.db.demandes.delete_one({'nom': nom})
    return jsonify({"status": "Deleted successfully"})

connexion_app.add_api('api.yml')
if __name__ == '__main__':
    app.run(debug=True, port=5001)
