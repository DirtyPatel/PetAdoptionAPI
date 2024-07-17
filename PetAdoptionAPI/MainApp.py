from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from faker import Faker

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/PetAdoptionDB"
mongo = PyMongo(app)
faker = Faker()

# List of common pet names
pet_names = [
    "Bella", "Luna", "Charlie", "Lucy", "Max", "Daisy", "Bailey", "Sadie", "Molly", "Buddy",
    "Rocky", "Zoe", "Chloe", "Coco", "Maggie", "Ruby", "Oscar", "Toby", "Jasper", "Finn"
]


# Generate fake pet data
def generate_fake_pet(id):
    pet = {
        "_id": id,
        "name": faker.random_element(elements=pet_names),
        "age": faker.random_int(min=1, max=15),
        "breed": faker.random_element(elements=("Labrador", "Persian", "Cockatiel", "Bulldog", "Beagle")),
        "type": faker.random_element(elements=("Dog", "Cat", "Bird")),
        "description": faker.random_element(
            elements=("Friendly", "Energetic", "Loves cuddles", "Loves playtime", "Loves to sleep")),
        "adoption_status": faker.random_element(elements=("Available", "Adopted"))
    }
    return pet


# Add a new pet
@app.route('/add_pet', methods=['POST'])
def add_pet():
    data = request.get_json()
    pet_id = mongo.db.pets.insert_one(data).inserted_id
    return jsonify(str(pet_id)), 201


# Get pet details by ID
@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = mongo.db.pets.find_one({"_id": id})
    if pet:
        pet['_id'] = str(pet['_id'])
        return jsonify(pet), 200
    else:
        return jsonify({"error": "Pet not found"}), 404


# Update pet information by ID
@app.route('/update_pet/<int:id>', methods=['PUT'])
def update_pet(id):
    data = request.get_json()
    result = mongo.db.pets.update_one({"_id": id}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Pet updated"}), 200
    else:
        return jsonify({"error": "Pet not found"}), 404


# Delete a pet by ID
@app.route('/delete_pet/<int:id>', methods=['DELETE'])
def delete_pet(id):
    result = mongo.db.pets.delete_one({"_id": id})
    if result.deleted_count:
        return jsonify({"message": "Pet deleted"}), 200
    else:
        return jsonify({"error": "Pet not found"}), 404


# Add sample pet data
@app.route('/add_sample_data', methods=['GET'])
def add_sample_data():
    mongo.db.pets.delete_many({})  # Clear the collection first
    sample_data = [generate_fake_pet(i) for i in range(1, 21)]  # Generate 20 fake pets with IDs 1-20
    result = mongo.db.pets.insert_many(sample_data)
    return jsonify({"inserted_ids": [str(id) for id in result.inserted_ids]}), 201


if __name__ == '__main__':
    app.run(debug=True)
