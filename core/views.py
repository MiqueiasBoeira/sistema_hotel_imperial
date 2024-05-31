from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quarto, Hospede, Checkin, Empresa, Checkout, Financeira, Reserva
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import CheckinForm, HospedeForm, EmpresaForm



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
    hospedes = Hospede.objects.filter(tipo_cliente='individual')
    empresas = Empresa.objects.all()

    if request.method == 'POST':
        form = CheckinForm(request.POST)
        tipo_hospede = request.POST.get('tipo_hospede')

        if form.is_valid():
            checkin = form.save(commit=False)

            if tipo_hospede == 'individual':
                hospede_principal = form.cleaned_data['hospede_principal']
                checkin.hospede_principal = hospede_principal

                # Adicionar hóspedes secundários
                hospedes_secundarios = request.POST.getlist('hospede_secundario')
                checkin.save()
                checkin.hospedes_secundarios.set(hospedes_secundarios)

            elif tipo_hospede == 'empresa':
                empresa = form.cleaned_data['empresa']
                checkin.empresa = empresa
                # Adicionar hóspedes da empresa
                hospedes_empresariais = request.POST.getlist('hospede_empresa')
                checkin.save()
                checkin.hospedes_secundarios.set(hospedes_empresariais)

            # Adicionar acompanhantes
            acompanhantes = form.cleaned_data['acompanhantes']
            checkin.acompanhantes = acompanhantes

            checkin.save()
            return redirect('pagina_inicial')
    else:
        form = CheckinForm()
    return render(request, 'core/checkin.html', {'form': form, 'hospedes': hospedes, 'empresas': empresas})


@login_required
def incluir_hospede_view(request):
    if request.method == 'POST':
        form = HospedeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkin')  # Redirecionar de volta ao formulário de check-in
    else:
        form = HospedeForm()
    return render(request, 'core/incluir_hospede.html', {'form': form})

@login_required
def gerenciar_hospedes_view(request):
    hospedes = Hospede.objects.all()
    return render(request, 'core/gerenciar_hospedes.html', {'hospedes': hospedes})


@login_required
def editar_hospede_view(request, pk):
    hospede = get_object_or_404(Hospede, pk=pk)
    if request.method == 'POST':
        form = HospedeForm(request.POST, instance=hospede)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_hospedes_view')
    else:
        form = HospedeForm(instance=hospede)
    return render(request, 'core/incluir_hospede.html', {'form': form})

@login_required
def excluir_hospede_view(request, pk):
    hospede = get_object_or_404(Hospede, pk=pk)
    if request.method == 'POST':
        hospede.delete()
        return redirect('gerenciar_hospedes_view')
    return render(request, 'core/excluir_hospede_confirm.html', {'hospede': hospede})



@login_required
def incluir_empresa_view(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkin')
    else:
        form = EmpresaForm()
    return render(request, 'core/incluir_empresa.html', {'form': form})

@login_required
def gerenciar_empresas_view(request):
    empresas = Empresa.objects.all()
    return render(request, 'core/gerenciar_empresas.html', {'empresas': empresas})

@login_required
def editar_empresa_view(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_empresas_view')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'core/incluir_empresa.html', {'form': form})

@login_required
def excluir_empresa_view(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        return redirect('gerenciar_empresas_view')
    return render(request, 'core/excluir_empresa_confirm.html', {'empresa': empresa})



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