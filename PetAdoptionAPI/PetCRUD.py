from flask import jsonify


class PetCRUD:
    def __init__(self, db):
        self.db = db
        self.pets = self.db.pets

    def add_pet(self, pet_data):
        pet_id = self.db.pets.insert_one(pet_data).inserted_id
        return str(pet_id)

    def get_pet(self, pet_id):
        pet = self.db.pets.find_one({"_id": pet_id})
        if pet:
            pet['_id'] = str(pet['_id'])
        return pet

    def update_pet(self, pet_id, data):
        result = self.db.pets.update_one({"_id": pet_id}, {"$set": data})
        return result.matched_count > 0

    def delete_pet(self, pet_id):
        result = self.db.pets.delete_one({"_id": pet_id})
        return result.deleted_count > 0

    def search_pets(self, query_params):
        query = {}
        if 'name' in query_params:
            query['name'] = query_params['name']
        if 'breed' in query_params:
            query['breed'] = query_params['breed']
        if 'adoption_status' in query_params:
            query['adoption_status'] = query_params['adoption_status']
        return list(self.db.pets.find(query))

    def add_sample_data(self):
        sample_data = [
            {"_id": 1, "name": "Bella", "age": 3, "breed": "Labrador", "type": "Dog", "description": "Friendly",
             "adoption_status": "Available"},
            {"_id": 2, "name": "Luna", "age": 2, "breed": "Persian", "type": "Cat", "description": "Loves to sleep",
             "adoption_status": "Adopted"},
            {"_id": 3, "name": "Charlie", "age": 4, "breed": "Beagle", "type": "Dog",
             "description": "Energetic and playful", "adoption_status": "Available"},
            {"_id": 4, "name": "Lucy", "age": 5, "breed": "Siamese", "type": "Cat", "description": "Affectionate",
             "adoption_status": "Adopted"},
            {"_id": 5, "name": "Max", "age": 1, "breed": "Cockatiel", "type": "Bird",
             "description": "Sings beautifully", "adoption_status": "Available"},
            {"_id": 6, "name": "Daisy", "age": 3, "breed": "Bulldog", "type": "Dog", "description": "Calm and gentle",
             "adoption_status": "Available"},
            {"_id": 7, "name": "Bailey", "age": 2, "breed": "Maine Coon", "type": "Cat", "description": "Very friendly",
             "adoption_status": "Adopted"},
            {"_id": 8, "name": "Sadie", "age": 4, "breed": "Golden Retriever", "type": "Dog",
             "description": "Loves to fetch", "adoption_status": "Available"},
            {"_id": 9, "name": "Molly", "age": 6, "breed": "Shih Tzu", "type": "Dog", "description": "Loves to cuddle",
             "adoption_status": "Adopted"},
            {"_id": 10, "name": "Buddy", "age": 3, "breed": "Poodle", "type": "Dog", "description": "Very smart",
             "adoption_status": "Available"},
            {"_id": 11, "name": "Rocky", "age": 5, "breed": "Rottweiler", "type": "Dog", "description": "Protective",
             "adoption_status": "Available"},
            {"_id": 12, "name": "Zoe", "age": 2, "breed": "Bengal", "type": "Cat", "description": "Active and curious",
             "adoption_status": "Adopted"},
            {"_id": 13, "name": "Chloe", "age": 1, "breed": "Cockapoo", "type": "Dog", "description": "Loves to play",
             "adoption_status": "Available"},
            {"_id": 14, "name": "Coco", "age": 4, "breed": "Pomeranian", "type": "Dog",
             "description": "Fluffy and cute", "adoption_status": "Adopted"},
            {"_id": 15, "name": "Maggie", "age": 3, "breed": "Tabby", "type": "Cat", "description": "Quiet and calm",
             "adoption_status": "Available"},
            {"_id": 16, "name": "Ruby", "age": 2, "breed": "Parakeet", "type": "Bird", "description": "Very colorful",
             "adoption_status": "Available"},
            {"_id": 17, "name": "Oscar", "age": 4, "breed": "Husky", "type": "Dog",
             "description": "Energetic and vocal", "adoption_status": "Adopted"},
            {"_id": 18, "name": "Toby", "age": 5, "breed": "Basset Hound", "type": "Dog",
             "description": "Loves to sniff", "adoption_status": "Available"},
            {"_id": 19, "name": "Jasper", "age": 3, "breed": "Sphynx", "type": "Cat", "description": "Very friendly",
             "adoption_status": "Available"},
            {"_id": 20, "name": "Finn", "age": 1, "breed": "Cocker Spaniel", "type": "Dog",
             "description": "Loves water", "adoption_status": "Adopted"},
            {"_id": 21, "name": "Chirpy", "age": 2, "breed": "Parakeet", "type": "Bird",
             "description": "Colorful and talkative", "adoption_status": "Adopted"},
            {"_id": 22, "name": "Fluffy", "age": 3, "breed": "Syrian", "type": "Hamster",
             "description": "Loves to burrow", "adoption_status": "Available"},
            {"_id": 23, "name": "Nibbles", "age": 1, "breed": "Dwarf", "type": "Hamster", "description": "Very playful",
             "adoption_status": "Available"},
            {"_id": 24, "name": "Thumper", "age": 2, "breed": "Lop", "type": "Rabbit", "description": "Loves to hop",
             "adoption_status": "Adopted"},
            {"_id": 25, "name": "BunBun", "age": 4, "breed": "Angora", "type": "Rabbit", "description": "Very fluffy",
             "adoption_status": "Available"},
            {"_id": 26, "name": "Snowball", "age": 2, "breed": "Rex", "type": "Rabbit",
             "description": "Gentle and calm", "adoption_status": "Available"}

        ]
        self.pets.delete_many({})  # Clear the collection first
        result = self.pets.insert_many(sample_data)
        return [str(id) for id in result.inserted_ids]
