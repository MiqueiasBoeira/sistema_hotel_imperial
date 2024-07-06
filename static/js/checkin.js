function toggleHospedeFields() {
    const tipoHospede = document.getElementById('tipo_hospede').value;
    document.getElementById('individual_fields').style.display = tipoHospede === 'individual' ? 'block' : 'none';
    document.getElementById('empresa_fields').style.display = tipoHospede === 'empresa' ? 'block' : 'none';
}

function searchHospede() {
    const query = document.getElementById('search_hospede').value.trim();

    // Se o campo de pesquisa estiver vazio, limpa os resultados e retorna.
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
    Array.from(results.children).forEach(child => child.classList.remove('selected'));  // Remove a classe de todos os itens
    event.target.classList.add('selected');  // Adiciona a classe ao item clicado
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

    // Se o campo de pesquisa estiver vazio, limpa os resultados e retorna.
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

function addIndividualHospedeField() {
    const hospedeFields = document.getElementById('individual_hospede_fields');
    const newField = document.createElement('div');
    newField.innerHTML = `
        <label for="hospede_secundario">Hóspede Secundário:</label>
        <select name="hospede_secundario">
            {% for hospede in hospedes %}
                <option value="{{ hospede.id }}">{{ hospede.nome_completo }}</option>
            {% endfor %}
        </select>
    `;
    hospedeFields.appendChild(newField);
}

function addEmpresaHospedeField() {
    const hospedeFields = document.getElementById('empresa_hospede_fields');
    const newField = document.createElement('div');
    newField.innerHTML = `
        <label for="hospede_empresa">Hóspede da Empresa:</label>
        <select name="hospede_empresa">
            {% for hospede in hospedes %}
                <option value="{{ hospede.id }}">{{ hospede.nome_completo }}</option>
            {% endfor %}
        </select>
    `;
    hospedeFields.appendChild(newField);
}
