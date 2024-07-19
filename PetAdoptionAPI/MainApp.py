from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from PetCRUD import PetCRUD

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/PetAdoptionDB"
mongo = PyMongo(app)
pet_crud = PetCRUD(mongo.db)


# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_pet', methods=['POST'])
def add_pet():
    data = request.get_json()
    pet_id = pet_crud.add_pet(data)
    return jsonify(pet_id), 201


@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = pet_crud.get_pet(id)
    if pet:
        return jsonify(pet), 200
    else:
        return jsonify({"error": "Pet not found"}), 404


@app.route('/update_pet/<int:id>', methods=['PUT'])
def update_pet(id):
    data = request.get_json()
    success = pet_crud.update_pet(id, data)
    if success:
        return jsonify({"message": "Pet updated"}), 200
    else:
        return jsonify({"error": "Pet not found"}), 404


@app.route('/delete_pet/<int:id>', methods=['DELETE'])
def delete_pet(id):
    success = pet_crud.delete_pet(id)
    if success:
        return jsonify({"message": "Pet deleted"}), 200
    else:
        return jsonify({"error": "Pet not found"}), 404


# API endpoint to add sample pet data
@app.route('/api/add_sample_data', methods=['GET'])
def add_sample_data():
    inserted_ids = pet_crud.add_sample_data()
    return jsonify({"inserted_ids": inserted_ids}), 201


@app.route('/api/search_pets', methods=['GET'])
def search_pets():
    query_params = request.args
    pets = pet_crud.search_pets(query_params)
    return jsonify(pets), 200


if __name__ == '__main__':
    app.run(debug=True)
