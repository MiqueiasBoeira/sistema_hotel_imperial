document.addEventListener('DOMContentLoaded', function() {
    var tipoClienteSelect = document.getElementById('tipo_cliente');
    var empresaInfo = document.getElementById('empresa_info');

    tipoClienteSelect.addEventListener('change', function() {
        if (this.value === 'empresa') {
            empresaInfo.style.display = 'block';
        } else {
            empresaInfo.style.display = 'none';
        }
    });
});

function toggleHospedeFields() {
    const tipoHospede = document.getElementById('tipo_hospede').value;
    document.getElementById('individual_fields').style.display = tipoHospede === 'individual' ? 'block' : 'none';
    document.getElementById('empresa_fields').style.display = tipoHospede === 'empresa' ? 'block' : 'none';
}

let hospedeCount = 0;

function addHospedeField() {
    hospedeCount++;
    const hospedeFields = document.getElementById('hospede_fields');
    const newField = document.createElement('div');
    newField.id = `hospede_${hospedeCount}`;
    newField.innerHTML = `
        <label for="hospede_${hospedeCount}">Hóspede ${hospedeCount}:</label>
        <input type="text" id="hospede_${hospedeCount}" name="hospede_${hospedeCount}">
    `;
    hospedeFields.appendChild(newField);
}

function removeHospedeField() {
    if (hospedeCount > 0) {
        const hospedeFields = document.getElementById('hospede_fields');
        const fieldToRemove = document.getElementById(`hospede_${hospedeCount}`);
        hospedeFields.removeChild(fieldToRemove);
        hospedeCount--;
    }
}