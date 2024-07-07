document.getElementById('checkin_id').addEventListener('change', function() {
    const checkinId = this.value;
    if (checkinId) {
        const checkinTipo = document.getElementById('checkin_tipo').value;
        fetch(`/get_checkin_details/${checkinId}/?checkin_tipo=${checkinTipo}`)
            .then(response => response.json())
            .then(data => {
                const detailsDiv = document.getElementById('checkin-details');
                detailsDiv.innerHTML = `
                    <h3>Detalhes do Check-in</h3>
                    <p><strong>Data de Check-in:</strong> ${data.checkin.data_checkin}</p>
                    <p><strong>Data de Check-out:</strong> ${data.checkin.data_checkout}</p>
                    <p><strong>Diária:</strong> ${data.checkin.diaria}</p>
                    <p><strong>Número de Dias:</strong> ${data.checkin.num_dias}</p>
                    <p><strong>Companhia:</strong> ${data.checkin.companhia}</p>
                    <p><strong>Motivo da Viagem:</strong> ${data.checkin.motivo_viagem}</p>
                    <p><strong>Acompanhantes:</strong> ${data.checkin.acompanhantes}</p>
                    <h3>Detalhes do Hóspede</h3>
                    <p><strong>Nome:</strong> ${data.hospede.nome_completo}</p>
                    <p><strong>CPF:</strong> ${data.hospede.cpf}</p>
                    <p><strong>E-mail:</strong> ${data.hospede.email}</p>
                    <p><strong>Telefone:</strong> ${data.hospede.telefone}</p>
                    <p><strong>Endereço:</strong> ${data.hospede.endereco}</p>
                    <p><strong>Tipo de Cliente:</strong> ${data.hospede.tipo_cliente}</p>
                    ${data.hospede.empresa ? `<p><strong>Empresa:</strong> ${data.hospede.empresa}</p>` : ''}
                `;
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('checkin-details').innerHTML = '';
    }
});
