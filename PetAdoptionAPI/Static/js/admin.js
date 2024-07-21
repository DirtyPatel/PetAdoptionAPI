document.addEventListener('DOMContentLoaded', function() {
    const petsList = document.getElementById('pets-list');
    const addPetForm = document.getElementById('add-pet-form');
    const showAllPetsButton = document.getElementById('show-all-pets-button');
     const editPetButton = document.getElementById('edit-pet-button');
    const deletePetButton = document.getElementById('delete-pet-button');
    let selectedPetId = null; // Track the selected pet ID

    // Function to fetch and display all pets
    function fetchAndDisplayPets() {
        console.log('Fetching all pets...'); // Debugging log
        fetch('/api/search_pets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({}) // Fetch all pets
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data fetched:', data); // Debugging log
            petsList.innerHTML = '';
            if (data.length > 0) {
                data.forEach(pet => {
                    let petItem = document.createElement('li');
                    petItem.classList.add('pet-item');
                    petItem.innerHTML = `
                        <h3>${pet.name}</h3>
                        <p><strong>Breed:</strong> ${pet.breed}</p>
                        <p><strong>Type:</strong> ${pet.type}</p>
                        <p><strong>Age:</strong> ${pet.age}</p>
                        <p><strong>Description:</strong> ${pet.description}</p>
                        <p><strong>Adoption Status:</strong> ${pet.adoption_status}</p>
                    `;
                    petItem.addEventListener('click', function() {
                        selectedPetId = pet._id;
                        populateForm(pet);
                        document.querySelectorAll('.pet-item').forEach(item => item.classList.remove('selected'));
                        petItem.classList.add('selected');
                    });
                    petsList.appendChild(petItem);
                });
            } else {
                petsList.innerHTML = '<p>No pets available.</p>';
            }
            petsList.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching pets');
        });
    }

    // Show all pets when the "Show All Pets" button is clicked
    showAllPetsButton.addEventListener('click', function() {
        console.log('Show All Pets button clicked'); // Debugging log
        fetchAndDisplayPets();
    });

    // Function to populate form with selected pet data
    function populateForm(pet) {
        addPetForm.name.value = pet.name;
        addPetForm.age.value = pet.age;
        addPetForm.breed.value = pet.breed;
        addPetForm.type.value = pet.type;
        addPetForm.description.value = pet.description;
        addPetForm.adoption_status.value = pet.adoption_status;
    }

    // Add event listener to "Add Pet" button
    addPetForm.addEventListener('submit', function(event) {
        event.preventDefault();
        let formData = new FormData(this);
        let jsonData = {};
        formData.forEach((value, key) => jsonData[key] = value);

        fetch('/add_pet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            alert('Pet added successfully');
            addPetForm.reset();
            fetchAndDisplayPets();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding pet');
        });
    });

    // Add event listener to "Edit Pet" button
    document.getElementById('edit-pet-button').addEventListener('click', function() {
        if (!selectedPetId) {
            alert('Please select a pet to edit');
            return;
        }

        let formData = new FormData(addPetForm);
        let jsonData = {};
        formData.forEach((value, key) => jsonData[key] = value);

        fetch(`/update_pet/${selectedPetId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })
         .then(response => response.json())
    .then(data => {
        if (data.status === 'Pet updated successfully') {
            alert('Pet updated successfully');
            addPetForm.reset();
            selectedPetId = null;
            fetchAndDisplayPets();
        } else {
            alert('Error updating pet');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating pet');
    });
});

    // Add event listener to "Delete Pet" button
    document.getElementById('delete-pet-button').addEventListener('click', function() {
        if (!selectedPetId) {
            alert('Please select a pet to delete');
            return;
        }

        fetch(`/delete_pet/${selectedPetId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Pet deleted successfully') {
                alert('Pet deleted successfully');
                selectedPetId = null;
                addPetForm.reset();
                fetchAndDisplayPets(); // Refresh the pets list
            } else {
                alert('Error deleting pet');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting pet');
        });
    });
});
