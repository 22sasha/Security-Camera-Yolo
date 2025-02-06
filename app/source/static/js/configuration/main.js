async function loadTextFields(newConfig) {
    const container = document.getElementById("list-connection-form");

    const newDiv = document.createElement('div');
    newDiv.className = 'connection-item';
    newDiv.id = `field-${newConfig.id}`;

    const idSpan = document.createElement('span');
    idSpan.textContent = `${newConfig.id}`;

    const newNameInput = document.createElement('input');
    newNameInput.type = 'text';
    newNameInput.value = newConfig.name;
    newNameInput.disabled = true;

    const newUrlInput = document.createElement('input');
    newUrlInput.type = 'text';
    newUrlInput.value = newConfig.url;
    newUrlInput.disabled = true;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Удалить';
    deleteButton.onclick = async function() {
        await deleteTextField(newConfig.id);
        newDiv.remove();
    };

    newDiv.appendChild(idSpan);
    newDiv.appendChild(newNameInput);
    newDiv.appendChild(newUrlInput);
    newDiv.appendChild(deleteButton);
    container.insertBefore(newDiv, container.firstChild);
}



async function addTextField() {
    const inputName = document.getElementById('newNameField');
    const name = inputName.value;

    const inputUrl = document.getElementById('newTextField');
    const url = inputUrl.value;
    
    if (url && name) {
        const response = await fetch(`camera_config`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: name, url: url }),
        });
        if (!response.ok) {
            console.error('Error adding url connection form:', await response.json());
        }
        const newConfig = await response.json();
        loadTextFields(newConfig.camera_config);
        inputName.value = '';
        inputUrl.value = '';
    }
}

async function deleteTextField(id) {
    const response = await fetch(`camera_config/${id}`, {
        method: "DELETE",
    });
    if (!response.ok) {
        console.error('Error deleting url connection form:', await response.json());
    }
    else {
        const divToRemove = document.getElementById(`field-${id}`);
        if (divToRemove) {
            divToRemove.remove();
        }
    }
}

async function changePage(page) {
    const response = await fetch(`/configuration?page=${page}`, {
        method: "GET",
    });
    if (response.ok) {
        const html = await response.text();
        document.body.innerHTML = html;
    } else {
        console.error('Error changing page:', await response.json());
    }
}