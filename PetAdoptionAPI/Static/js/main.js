document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display pet data
    fetch('/api/pets')
        .then(response => response.json())
        .then(data => {
            let petsList = document.getElementById('pets-list');
            data.forEach(pet => {
                let petItem = document.createElement('li');
                petItem.innerHTML = `
                    <h3>${pet.name}</h3>
                    <p><strong>Breed:</strong> ${pet.breed}</p>
                    <p><strong>Type:</strong> ${pet.type}</p>
                    <p><strong>Age:</strong> ${pet.age}</p>
                    <p><strong>Description:</strong> ${pet.description}</p>
                    <p><strong>Adoption Status:</strong> ${pet.adoption_status}</p>
                `;
                petsList.appendChild(petItem);
            });
        })
        .catch(error => console.error('Error fetching pet data:', error));

    // Handle add pet form submission
    document.getElementById('add-pet-form').addEventListener('submit', function(event) {
        event.preventDefault();
        let formData = new FormData(this);
        let petData = {};
        formData.forEach((value, key) => petData[key] = value);

        fetch('/add_pet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(petData)
        })
        .then(response => response.json())
        .then(data => {
            alert('Pet added successfully!');
            location.reload(); // Reload the page to see the new pet in the list
        })
        .catch(error => console.error('Error adding pet:', error));
    });
});
