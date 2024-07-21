document.addEventListener('DOMContentLoaded', function () {
    const petsList = document.getElementById('pets-list');
    const addPetForm = document.getElementById('add-pet-form');
// Function to fetch and display pets based on type
    function fetchAndDisplayPets(type) {
        let queryType;
        if (type === 'Other') {
            queryType = ['Bird', 'Hamster', 'Rabbit'];
        } else {
            queryType = [type];
        }

        fetch('/api/search_pets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ types: queryType })
        })
            .then(response => response.json())
            .then(data => {
                petsList.innerHTML = '';
                if (data.length > 0) {
                    data.forEach(pet => {
                        let petItem = document.createElement('li');
                        petItem.classList.add('pet-container');
                        petItem.innerHTML = `
                            <h3>${pet.name}</h3>
                            <p><strong>Breed:</strong> ${pet.breed}</p>
                            <p><strong>Type:</strong> ${pet.type}</p>
                            <p><strong>Age:</strong> ${pet.age}</p>
                            <p><strong>Description:</strong> ${pet.description}</p>
                            <p><strong>Adoption Status:</strong> ${pet.adoption_status}</p>
                            <button class="adopt-button" data-name="${pet.name}">Adopt Me</button>
                        `;
                        petsList.appendChild(petItem);
                    });

                    // Add event listeners for the "Adopt" buttons
                    document.querySelectorAll('.adopt-button').forEach(button => {
                        button.addEventListener('click', function () {
                            const petName = this.getAttribute('data-name');
                            alert(`Thank you for your interest in ${petName}. Pet adopted successfully!`);
                        });
                    });
                } else {
                    petsList.innerHTML = '<p>No pets available.</p>';
                }
                petsList.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching pets:', error);
            });
    }

    // Add event listeners to filter buttons
    document.querySelectorAll('.filter-button').forEach(button => {
        button.addEventListener('click', function () {
            // Remove active class from all buttons
            document.querySelectorAll('.filter-button').forEach(btn => btn.classList.remove('active'));
            // Add active class to the clicked button
            this.classList.add('active');
            // Fetch and display pets based on the type
            const type = this.getAttribute('data-type');
            fetchAndDisplayPets(type);
        });
    });
});