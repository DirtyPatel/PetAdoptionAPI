from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
from PetCRUD import PetCRUD  # Import PetCRUD class

app = Flask(__name__, static_folder='static')

client = MongoClient('mongodb://localhost:27017/')
db = client['PetAdoptionDB']
pets_collection = db['pets']

# Initialize PetCRUD class
pet_crud = PetCRUD(db)

pets = list(pets_collection.find())
print(pets)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/api/search_pets', methods=['POST'])
def search_pets():
    try:
        query_params = request.json
        types = query_params.get('types', [])
        query = {'type': {'$in': types}} if types else {}
        pets = list(pets_collection.find(query))
        for pet in pets:
            pet['_id'] = str(pet['_id'])  # Convert ObjectId to string
        return jsonify(pets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/add_pet', methods=['POST'])
def add_pet():
    pet_data = request.json
    pets_collection.insert_one(pet_data)
    return jsonify({'status': 'Pet added successfully'})


@app.route('/update_pet/<pet_id>', methods=['PUT'])
def update_pet(pet_id):
    updated_data = request.json
    try:
        pets_collection.update_one({'_id': ObjectId(pet_id)}, {'$set': updated_data})
        return jsonify({'status': 'Pet updated successfully'})
    except Exception as e:
        return jsonify({'status': 'Error updating pet', 'error': str(e)}), 500


@app.route('/delete_pet/<pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    try:
        pets_collection.delete_one({'_id': ObjectId(pet_id)})
        return jsonify({'status': 'Pet deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'Error deleting pet', 'error': str(e)}), 500


@app.route('/add_sample_data', methods=['GET'])
def add_sample_data():
    added_ids = pet_crud.add_sample_data()
    return jsonify({'status': 'Sample data added successfully', 'ids': added_ids})


if __name__ == '__main__':
    app.run(debug=True)
