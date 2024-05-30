from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quarto, Hospede, Checkin, Empresa, Checkout, Financeira, Reserva
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pagina_inicial')
        else:
            return render(request, 'core/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'core/login.html')



@login_required
def pagina_inicial(request):
    quartos = Quarto.objects.select_related('hospede', 'checkin').all()
    for quarto in quartos:
        hospede = quarto.hospede.nome_completo if quarto.hospede else "None"
        data_checkin = quarto.checkin.data_checkin if quarto.checkin else "None"
        data_checkout = quarto.checkin.data_checkout if quarto.checkin else "None"
        print(f'Quarto {quarto.numero_quarto} - Hóspede: {hospede} - Check-in: {data_checkin} - Check-out: {data_checkout}')
    context = {
        'quartos': quartos
    }
    return render(request, 'core/pagina_inicial.html', context)


@login_required
def checkin_view(request):
    if request.method == 'POST':
        nome_completo = request.POST['nome_completo']
        cpf = request.POST['cpf']
        email = request.POST['email']
        telefone = request.POST['telefone']
        endereco = request.POST['endereco']
        motivo_viagem = request.POST['motivo_viagem']
        diaria = request.POST['diaria']
        num_dias = request.POST['num_dias']
        data_checkin = request.POST['data_checkin']
        companhia = request.POST['companhia']
        numero_total_hospedes = request.POST['numero_total_hospedes']
        quarto_id = request.POST['quarto_id']
        tipo_cliente = request.POST['tipo_cliente']

        empresa = None
        if tipo_cliente == 'empresa':
            nome_empresa = request.POST['nome_empresa']
            cnpj = request.POST['cnpj']
            empresa, created = Empresa.objects.get_or_create(
                cnpj=cnpj,
                defaults={'nome_empresa': nome_empresa}
            )

        hospede, created = Hospede.objects.get_or_create(
            cpf=cpf,
            defaults={
                'nome_completo': nome_completo,
                'email': email,
                'telefone': telefone,
                'endereco': endereco,
                'tipo_cliente': tipo_cliente,
                'empresa': empresa
            }
        )

        checkin = Checkin.objects.create(
            hospede=hospede,
            quarto_id=quarto_id,
            data_checkin=data_checkin,
            diaria=diaria,
            num_dias=num_dias,
            companhia=companhia,
            motivo_viagem=motivo_viagem,
            numero_total_hospedes=numero_total_hospedes
        )

        quarto = Quarto.objects.get(id=quarto_id)
        quarto.estado = 'ocupado'
        quarto.save()

        return redirect('pagina_inicial')

    quartos = Quarto.objects.filter(estado='livre')
    return render(request, 'core/checkin.html', {'quartos': quartos})



@login_required
def checkout_view(request):
    if request.method == 'POST':
        checkin_id = request.POST['checkin_id']
        consumo = request.POST['consumo']
        observacoes = request.POST['observacoes']
        metodo_pagamento = request.POST['metodo_pagamento']
        total_pago = request.POST['total_pago']
        data_checkout = request.POST['data_checkout']

        checkin = Checkin.objects.get(id=checkin_id)

        checkout = Checkout.objects.create(
            checkin=checkin,
            data_checkout=data_checkout,
            consumo=consumo,
            observacoes=observacoes,
            metodo_pagamento=metodo_pagamento,
            total_pago=total_pago
        )

        Financeira.objects.create(
            tipo='receita',
            descricao=f'Checkout do quarto {checkin.quarto.numero_quarto}',
            valor=total_pago,
            data=data_checkout
        )

        quarto = checkin.quarto
        quarto.estado = 'livre'
        quarto.save()

        return redirect('pagina_inicial')

    checkins = Checkin.objects.filter(quarto__estado='ocupado')
    return render(request, 'core/checkout.html', {'checkins': checkins})

@login_required
def reserva_view(request):
    if request.method == 'POST':
        data_inicio = request.POST['data_inicio']
        data_fim = request.POST['data_fim']
        quarto_id = request.POST['quarto_id']
        hospede_id = request.POST.get('hospede_id')

        # Verifique se há conflito de reservas para o quarto selecionado
        reservas_conflitantes = Reserva.objects.filter(
            quarto_id=quarto_id,
            data_fim__gte=data_inicio,
            data_inicio__lte=data_fim
        )

        if reservas_conflitantes.exists():
            messages.error(request, "O quarto selecionado já está reservado para este período.")
            return redirect('reserva')

        # Crie a nova reserva se não houver conflitos
        reserva = Reserva.objects.create(
            data_inicio=data_inicio,
            data_fim=data_fim,
            quarto_id=quarto_id,
            hospede_id=hospede_id
        )

        messages.success(request, "Reserva criada com sucesso!")
        return redirect('pagina_inicial')

    quartos = Quarto.objects.all()
    hospedes = Hospede.objects.all()
    return render(request, 'core/reserva.html', {'quartos': quartos, 'hospedes': hospedes})
@login_required
def quarto_detalhes(request, quarto_id):
    quarto = get_object_or_404(Quarto, id=quarto_id)
    reservas = Reserva.objects.filter(quarto=quarto).order_by('data_inicio')
    return render(request, 'core/quarto_detalhes.html', {'quarto': quarto, 'reservas': reservas})

@login_required
@permission_required('core.view_financeira', raise_exception=True)
def financas_view(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        data = request.POST['data']

        Financeira.objects.create(
            tipo=tipo,
            descricao=descricao,
            valor=valor,
            data=data
        )

        return redirect('financas')

    transacoes = Financeira.objects.all().order_by('-data')
    return render(request, 'core/financas.html', {'transacoes': transacoes})