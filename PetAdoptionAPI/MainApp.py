from bson.errors import InvalidId
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
        pets = pet_crud.search_pets(query_params)
        return jsonify(pets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/add_pet', methods=['POST'])
def add_pet():
    try:
        pet_data = request.json
        pet_id = pet_crud.add_pet(pet_data)
        return jsonify({'status': 'Pet added successfully', 'pet_id': pet_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_pet/<pet_id>', methods=['PUT'])
def update_pet(pet_id):
    updated_data = request.json
    try:
        pet_id_to_be_updated = int(pet_id)
        result = pets_collection.update_one({'_id': pet_id_to_be_updated}, {'$set': updated_data})
        if result.matched_count > 0:
            return jsonify({'status': 'Pet updated successfully'})
        else:
            return jsonify({'status': 'Pet not found'}), 404
    except Exception as e:
        return jsonify({'status': 'Error updating pet', 'error': str(e)}), 500


@app.route('/delete_pet/<pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pet_id_to_be_deleted = int(pet_id)
    try:
        result = pets_collection.delete_one({'_id': pet_id_to_be_deleted})
        if result.deleted_count > 0:
            return jsonify({'status': 'Pet deleted successfully'})
        else:
            return jsonify({'status': 'Pet not found'}), 404
    except InvalidId as e:
        return jsonify({'status': 'Error deleting pet', 'error': 'Invalid pet ID format'}), 400
    except Exception as e:
        return jsonify({'status': 'Error deleting pet', 'error': str(e)}), 500


@app.route('/add_sample_data', methods=['GET'])
def add_sample_data():
    try:
        added_ids = pet_crud.add_sample_data()
        return jsonify({'status': 'Sample data added successfully', 'ids': added_ids})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
