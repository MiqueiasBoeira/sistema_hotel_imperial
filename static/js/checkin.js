function toggleHospedeFields() {
    const tipoHospede = document.getElementById('tipo_hospede').value;
    document.getElementById('individual_fields').style.display = tipoHospede === 'individual' ? 'block' : 'none';
    document.getElementById('empresa_fields').style.display = tipoHospede === 'empresa' ? 'block' : 'none';
}

function searchHospede() {
    const query = document.getElementById('search_hospede').value.trim();

    if (query === "") {
        document.getElementById('search_results').innerHTML = '';
        return;
    }

    fetch(`/search_hospede/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const results = document.getElementById('search_results');
            results.innerHTML = '';
            data.forEach(hospede => {
                const li = document.createElement('li');
                li.textContent = `${hospede.nome_completo} - ${hospede.cpf}`;
                li.onclick = () => selectHospede(hospede.id, hospede.nome_completo);
                results.appendChild(li);
            });
        });
}
function selectHospede(id, nome_completo) {
    document.getElementById('search_hospede').value = nome_completo;
    document.getElementById('selected_hospede_id').value = id;
    const results = document.getElementById('search_results');
    Array.from(results.children).forEach(child => child.classList.remove('selected'));
    event.target.classList.add('selected');
    results.innerHTML = '';
}

function confirmHospedeSelection() {
    const selectedHospede = document.getElementById('selected_hospede_id').value;
    if (selectedHospede) {
        alert("Hóspede selecionado com sucesso!");
    } else {
        alert("Por favor, selecione um hóspede.");
    }
}

function searchEmpresa() {
    const query = document.getElementById('search_empresa').value.trim();

    if (query === "") {
        document.getElementById('search_empresa_results').innerHTML = '';
        return;
    }

    fetch(`/search_empresa/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const results = document.getElementById('search_empresa_results');
            results.innerHTML = '';
            data.forEach(empresa => {
                const li = document.createElement('li');
                li.textContent = `${empresa.nome_empresa} - ${empresa.cnpj}`;
                li.onclick = () => selectEmpresa(empresa.id, empresa.nome_empresa);
                results.appendChild(li);
            });
        });
}

function selectEmpresa(id, nome_empresa) {
    document.getElementById('search_empresa').value = nome_empresa;
    document.getElementById('selected_empresa_id').value = id;
    document.getElementById('search_empresa_results').innerHTML = '';
}

function confirmEmpresaSelection() {
    const selectedEmpresa = document.getElementById('selected_empresa_id').value;
    if (selectedEmpresa) {
        alert("Empresa selecionada com sucesso!");
    } else {
        alert("Por favor, selecione uma empresa.");
    }
}

function searchHospedeEmpresa(input) {
    const query = input.value.trim();

    if (query === "") {
        input.nextElementSibling.innerHTML = '';
        return;
    }

    fetch(`/search_hospede/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const results = input.nextElementSibling;
            results.innerHTML = '';
            data.forEach(hospede => {
                const li = document.createElement('li');
                li.textContent = `${hospede.nome_completo} - ${hospede.cpf}`;
                li.onclick = () => selectHospedeEmpresa(hospede.id, hospede.nome_completo, input);
                results.appendChild(li);
            });
        });
}

function selectHospedeEmpresa(id, nome_completo, input) {
    input.value = nome_completo;
    input.nextElementSibling.nextElementSibling.value = id;
    input.nextElementSibling.innerHTML = '';
}

function confirmHospedeEmpresaSelection(button) {
    const selectedHospedeEmpresaId = button.previousElementSibling.value;
    if (selectedHospedeEmpresaId) {
        alert("Hóspede da empresa selecionado com sucesso!");
    } else {
        alert("Por favor, selecione um hóspede da empresa.");
    }
}

function addIndividualHospedeField() {
    const hospedeFields = document.getElementById('individual_hospede_fields');
    const newField = document.createElement('div');
    newField.classList.add('hospede-secundario-field');
    newField.innerHTML = `
        <input type="text" class="search_hospede_secundario" oninput="searchHospedeSecundario(this)">
        <ul class="search_hospede_secundario_results"></ul>
        <input type="hidden" class="selected_hospede_secundario_id" name="hospedes_secundarios_ids">
        <button type="button" onclick="confirmHospedeSecundarioSelection(this)">Confirmar Hóspede Secundário</button>
    `;
    hospedeFields.appendChild(newField);
}


function addEmpresaHospedeField() {
    const hospedeFields = document.getElementById('empresa_hospede_fields');
    const newField = document.createElement('div');
    newField.classList.add('hospede-secundario-field');
    newField.innerHTML = `
        <input type="text" class="search_hospede_secundario" oninput="searchHospedeSecundario(this)">
        <ul class="search_hospede_secundario_results"></ul>
        <input type="hidden" class="selected_hospede_secundario_id" name="hospedes_secundarios_ids">
        <button type="button" onclick="confirmHospedeSecundarioSelection(this)">Confirmar Hóspede Secundário</button>
    `;
    hospedeFields.appendChild(newField);
}


function searchHospedeSecundario(input) {
    const query = input.value.trim();
    if (query === "") {
        input.nextElementSibling.innerHTML = '';
        return;
    }

    fetch(`/search_hospede/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const results = input.nextElementSibling;
            results.innerHTML = '';
            data.forEach(hospede => {
                const li = document.createElement('li');
                li.textContent = `${hospede.nome_completo} - ${hospede.cpf}`;
                li.onclick = (event) => selectHospedeSecundario(hospede.id, hospede.nome_completo, input, event);
                results.appendChild(li);
            });
        });
}


function selectHospedeSecundario(id, nome_completo, input, event) {
    input.value = nome_completo;
    input.nextElementSibling.nextElementSibling.value = id;
    const results = input.nextElementSibling;
    Array.from(results.children).forEach(child => child.classList.remove('selected'));
    event.target.classList.add('selected');
    results.innerHTML = '';
}


function confirmHospedeSecundarioSelection(button) {
    const selectedHospedeSecundarioId = button.previousElementSibling.value;
    if (selectedHospedeSecundarioId) {
        alert("Hóspede secundário selecionado com sucesso!");
    } else {
        alert("Por favor, selecione um hóspede secundário.");
    }
}
