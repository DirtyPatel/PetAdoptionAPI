document.addEventListener('DOMContentLoaded', function() {
    const addPetForm = document.getElementById('add-pet-form');

    if (addPetForm) {
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
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error adding pet');
            });
        });
    }
});
