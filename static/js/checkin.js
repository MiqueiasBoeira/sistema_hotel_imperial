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
