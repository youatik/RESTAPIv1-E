
from flask_pymongo import PyMongo
from flask import jsonify, request, abort
import connexion
from pymongo.errors import DuplicateKeyError

# Initialiser l'application connexion
connexion_app = connexion.App(__name__, specification_dir='./')
app = connexion_app.app

# Configuration de MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/A15"
mongo = PyMongo(app)

# Récupérer tous les employés
@app.route('/v1/employes', methods=['GET'])
def get_employes():
    employes = mongo.db.employes.find()
    result = []
    for employe in employes:
        employe['_id'] = str(employe['_id'])
        result.append(employe)
    return jsonify(result)

# Ajouter un employé
@app.route('/v1/employes', methods=['POST'])
def add_employe():
    employe = request.json

    demandes = employe.get('demandes', [])

    for demande_nom in demandes:
        demande = mongo.db.demandes.find_one({'nom': demande_nom})
        if not demande:
            abort(400, f"No demande found with the name {demande_nom}")

    result = mongo.db.employes.insert_one(employe)

    return jsonify({"_id": str(result.inserted_id)})

# Récupérer un employé par son numéro
@app.route('/v1/employes/numero/<numero>', methods=['GET'])
def get_single_employe_by_numero(numero):
    employe = mongo.db.employes.find_one({'numero': numero})
    if not employe:
        return jsonify({"error": "Employe not found"}), 404
    employe['_id'] = str(employe['_id'])
    return jsonify(employe)

# Mettre à jour un employé par son numéro
@app.route('/v1/employes/numero/<numero>', methods=['PUT'])
def update_employe_by_numero(numero):
    employe_data = request.json

    if 'demandes' not in employe_data:
        abort(400, "The 'demandes' key must be present, even if the array is empty.")

    for demande_nom in employe_data['demandes']:
        demande_in_db = mongo.db.demandes.find_one({'nom': demande_nom})
        if not demande_in_db:
            abort(400, f"The demande with nom '{demande_nom}' does not exist.")

    mongo.db.employes.update_one({'numero': numero}, {"$set": employe_data})

    return jsonify({"status": "Updated successfully"})

# Supprimer un employé par son numéro
@app.route('/v1/employes/numero/<numero>', methods=['DELETE'])
def delete_employe_by_numero(numero):
    mongo.db.employes.delete_one({'numero': numero})
    return jsonify({"status": "Deleted successfully"})

# Récupérer tous les projets
@app.route('/v1/projets', methods=['GET'])
def get_projets():
    projets = mongo.db.projets.find()
    result = []
    for projet in projets:
        projet['_id'] = str(projet['_id'])
        result.append(projet)
    return jsonify(result)

# Ajouter un projet
@app.route('/v1/projets', methods=['POST'])
def add_projet():
    projet = request.json

    demandes_noms = projet.get('demandes_traitees', [])

    existing_demandes_count = mongo.db.demandes.count_documents({"nom": {"$in": demandes_noms}})

    if existing_demandes_count != len(demandes_noms):
        return jsonify({"error": "One or more demandes do not exist in A15.demandes based on the provided 'nom' values"}), 400

    try:
        result = mongo.db.projets.insert_one(projet)
        return jsonify({"_id": str(result.inserted_id)})
    except DuplicateKeyError:
        return jsonify({"error": "Projet with the same ID already exists"}), 400



# Récupérer un projet par son code
@app.route('/v1/projets/code/<code>', methods=['GET'])
def get_single_projet_by_code(code):
    projet = mongo.db.projets.find_one({'code': code})
    if not projet:
        return jsonify({"error": "Projet not found"}), 404
    projet['_id'] = str(projet['_id'])
    return jsonify(projet)

# Mettre à jour un projet par son code
@app.route('/v1/projets/code/<code>', methods=['PUT'])
def update_projet_by_code(code):
    projet_data = request.json

    demandes_noms = projet_data.get('demandes_traitees', [])

    existing_demandes_count = mongo.db.demandes.count_documents({"nom": {"$in": demandes_noms}})

    if existing_demandes_count != len(demandes_noms):
        return jsonify({"error": "One or more demandes do not exist in A15.demandes based on the provided 'nom' values"}), 400

    result = mongo.db.projets.update_one({'code': code}, {"$set": projet_data})

    if result.matched_count == 0:
        return jsonify({"error": "No project found with the provided code"}), 404

    return jsonify({"status": "Updated successfully"})


# Supprimer un projet par son code
@app.route('/v1/projets/code/<code>', methods=['DELETE'])
def delete_projet_by_code(code):
    mongo.db.projets.delete_one({'code': code})
    return jsonify({"status": "Deleted successfully"})

# Récupérer toutes les demandes
@app.route('/v1/demandes', methods=['GET'])
def get_demandes():
    demandes = mongo.db.demandes.find()
    result = []
    for demande in demandes:
        demande['_id'] = str(demande['_id'])
        result.append(demande)
    return jsonify(result)

# Ajouter une demande
@app.route('/v1/demandes', methods=['POST'])
def add_demande():
    demande = request.json

    employe_id = demande.get("employe_id")
    projet_id = demande.get("projet_id")

    if employe_id:
        employe = mongo.db.employes.find_one({"numero": employe_id})
        if not employe:
            abort(400, "Invalid employe_id")

    if projet_id:
        projet = mongo.db.projets.find_one({"code": projet_id})
        if not projet:
            abort(400, "Invalid projet_id")

    result = mongo.db.demandes.insert_one(demande)

    return jsonify({"_id": str(result.inserted_id)})

# Récupérer une demande par son nom
@app.route('/v1/demandes/nom/<nom>', methods=['GET'])
def get_single_demande_by_nom(nom):
    demande = mongo.db.demandes.find_one({'nom': nom})
    if not demande:
        return jsonify({"error": "Demande not found"}), 404
    demande['_id'] = str(demande['_id'])
    return jsonify(demande)

# Mettre à jour une demande par son nom
@app.route('/v1/demandes/nom/<nom>', methods=['PUT'])
def update_demande_by_nom(nom):
    demande_data = request.json

    employe_id = demande_data.get("employe_id")
    projet_id = demande_data.get("projet_id")

    if employe_id is not None:
        employe = mongo.db.employes.find_one({"numero": employe_id})
        if not employe:
            abort(400, "Invalid employe_id")

    if projet_id is not None:
        projet = mongo.db.projets.find_one({"code": projet_id})
        if not projet:
            abort(400, "Invalid projet_id")

    mongo.db.demandes.update_one({'nom': nom}, {"$set": demande_data})

    return jsonify({"status": "Updated successfully"})

# Supprimer une demande par son nom
@app.route('/v1/demandes/nom/<nom>', methods=['DELETE'])
def delete_demande_by_nom(nom):
    mongo.db.demandes.delete_one({'nom': nom})
    return jsonify({"status": "Deleted successfully"})

connexion_app.add_api('api.yml')
if __name__ == '__main__':
    app.run(debug=True, port=5001)
