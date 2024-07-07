from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quarto, Hospede, CheckinIndividual, CheckinEmpresa, Empresa, Checkout, Financeira, Reserva

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import CheckinIndividualForm, CheckinEmpresaForm, HospedeForm, EmpresaForm, FinanceiroForm
import logging

logger = logging.getLogger(__name__)



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
    quartos = Quarto.objects.select_related('hospede', 'checkin_individual', 'checkin_empresa').all()

    for quarto in quartos:
        if quarto.checkin_empresa:
            quarto.empresa = quarto.checkin_empresa.empresa

    context = {
        'quartos': quartos
    }
    return render(request, 'core/pagina_inicial.html', context)


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

from django.shortcuts import render, redirect, get_object_or_404
from .models import Quarto, Hospede, CheckinIndividual, CheckinEmpresa, Empresa, Checkout, Financeira, Reserva
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CheckinIndividualForm, CheckinEmpresaForm, HospedeForm, EmpresaForm, FinanceiroForm
from django.http import JsonResponse

@login_required
def checkin_view(request):
    hospedes = Hospede.objects.all()
    empresas = Empresa.objects.all()
    quartos_livres = Quarto.objects.filter(estado='livre')

    if request.method == 'POST':
        tipo_hospede = request.POST.get('tipo_hospede')
        form_individual = None
        form_empresa = None
        if tipo_hospede == 'individual':
            form_individual = CheckinIndividualForm(request.POST)
            if form_individual.is_valid():
                checkin = form_individual.save(commit=False)
                hospede_id = request.POST.get('selected_hospede_id')
                if hospede_id:
                    hospede_principal = get_object_or_404(Hospede, id=hospede_id)
                    checkin.hospede_principal = hospede_principal
                    checkin.save()
                    hospedes_secundarios = form_individual.cleaned_data['hospedes_secundarios']
                    checkin.hospedes_secundarios.set(hospedes_secundarios)
                    quarto = checkin.quarto
                    quarto.estado = 'ocupado'
                    quarto.checkin_individual = checkin
                    quarto.hospede = hospede_principal
                    quarto.tipo_checkin = 'individual'
                    quarto.save()
                    return redirect('pagina_inicial')
                else:
                    form_individual.add_error(None, 'Selecione um hóspede principal')
        elif tipo_hospede == 'empresa':
            form_empresa = CheckinEmpresaForm(request.POST)
            if form_empresa.is_valid():
                checkin = form_empresa.save(commit=False)
                empresa_id = request.POST.get('selected_empresa_id')
                hospede_id = request.POST.get('selected_hospede_empresa_id')
                if empresa_id and hospede_id:
                    empresa = get_object_or_404(Empresa, id=empresa_id)
                    hospede_principal = get_object_or_404(Hospede, id=hospede_id)
                    checkin.empresa = empresa
                    checkin.hospede_principal = hospede_principal
                    checkin.save()
                    hospedes_secundarios = form_empresa.cleaned_data['hospedes_secundarios']
                    checkin.hospedes_secundarios.set(hospedes_secundarios)
                    quarto = checkin.quarto
                    quarto.estado = 'ocupado'
                    quarto.checkin_empresa = checkin
                    quarto.hospede = hospede_principal
                    quarto.tipo_checkin = 'empresa'
                    quarto.save()
                    return redirect('pagina_inicial')
                else:
                    form_empresa.add_error(None, 'Selecione uma empresa e um hóspede principal para a empresa')
    else:
        form_individual = CheckinIndividualForm()
        form_empresa = CheckinEmpresaForm()

    return render(request, 'core/checkin.html', {
        'form_individual': form_individual,
        'form_empresa': form_empresa,
        'hospedes': hospedes,
        'empresas': empresas,
        'quartos': quartos_livres
    })

@login_required
def search_hospede(request):
    query = request.GET.get('q', '')
    hospedes = Hospede.objects.filter(nome_completo__icontains=query)
    results = [{'id': hospede.id, 'nome_completo': hospede.nome_completo, 'cpf': hospede.cpf} for hospede in hospedes]
    return JsonResponse(results, safe=False)

@login_required
def search_empresa(request):
    query = request.GET.get('q', '')
    empresas = Empresa.objects.filter(nome_empresa__icontains=query)
    results = [{'id': empresa.id, 'nome_empresa': empresa.nome_empresa, 'cnpj': empresa.cnpj} for empresa in empresas]
    return JsonResponse(results, safe=False)



@login_required
def checkout_view(request):
    checkins_individuais_ativos = CheckinIndividual.objects.filter(quarto__estado='ocupado').exclude(
        id__in=Checkout.objects.values('checkin_individual_id'))
    checkins_empresas_ativos = CheckinEmpresa.objects.filter(quarto__estado='ocupado').exclude(
        id__in=Checkout.objects.values('checkin_empresa_id'))

    if request.method == 'POST':
        checkin_tipo = request.POST.get('checkin_tipo')
        checkin_id = request.POST.get('checkin_id')
        consumo = request.POST['consumo']
        observacoes = request.POST['observacoes']
        metodo_pagamento = request.POST['metodo_pagamento']
        total_pago = request.POST['total_pago']
        data_checkout = request.POST['data_checkout']

        if checkin_tipo == 'individual':
            checkin = get_object_or_404(CheckinIndividual, id=checkin_id)
        elif checkin_tipo == 'empresa':
            checkin = get_object_or_404(CheckinEmpresa, id=checkin_id)

        checkout = Checkout.objects.create(
            checkin_individual=checkin if checkin_tipo == 'individual' else None,
            checkin_empresa=checkin if checkin_tipo == 'empresa' else None,
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

    return render(request, 'core/checkout.html',
                  {'checkins_individuais': checkins_individuais_ativos, 'checkins_empresas': checkins_empresas_ativos})


@login_required
def reserva_view(request):
    if request.method == 'POST':
        quarto_id = request.POST['quarto_id']
        data_inicio = request.POST['data_inicio']
        data_fim = request.POST['data_fim']
        hospede_id = request.POST.get('hospede_id')
        nome_hospede = request.POST.get('nome_hospede')
        contato_hospede = request.POST.get('contato_hospede')

        quarto = Quarto.objects.get(id=quarto_id)

        if hospede_id:
            hospede = Hospede.objects.get(id=hospede_id)
            nome_hospede = hospede.nome_completo
            contato_hospede = hospede.telefone
        else:
            hospede = None

        reserva = Reserva.objects.create(
            quarto=quarto,
            hospede=hospede,
            nome_hospede=nome_hospede,
            contato_hospede=contato_hospede,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return redirect('pagina_inicial')

    hospedes = Hospede.objects.all()
    quartos = Quarto.objects.all()
    return render(request, 'core/reserva.html', {'hospedes': hospedes, 'quartos': quartos})

@login_required
def quarto_detalhes(request, id):
    quarto = get_object_or_404(Quarto, id=id)
    reservas = quarto.reservas.filter(status='ativo')

    if request.method == 'POST' and 'cancelar_reserva' in request.POST:
        reserva_id = request.POST['reserva_id']
        reserva = get_object_or_404(Reserva, id=reserva_id)
        reserva.status = 'cancelado'
        reserva.save()
        return redirect('quarto_detalhes', id=quarto.id)

    context = {
        'quarto': quarto,
        'reservas': reservas
    }
    return render(request, 'core/quarto_detalhes.html', context)


@login_required
@permission_required('core.view_financeira', raise_exception=True)
def financeiro_view(request):
    form = FinanceiroForm()
    lancamentos = Financeira.objects.all()

    if request.method == 'POST' and 'tipo' in request.POST:
        # Lógica para adicionar uma nova transação
        tipo = request.POST['tipo']
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        data = request.POST['data']
        Financeira.objects.create(tipo=tipo, descricao=descricao, valor=valor, data=data)
    elif request.method == 'POST' and 'data_inicial' in request.POST:
        # Lógica para filtrar os lançamentos financeiros
        form = FinanceiroForm(request.POST)
        if form.is_valid():
            data_inicial = form.cleaned_data['data_inicial']
            data_final = form.cleaned_data['data_final']
            lancamentos = Financeira.objects.filter(data__range=[data_inicial, data_final])

    return render(request, 'core/financas.html', {'form': form, 'lancamentos': lancamentos})


def get_checkin_details(request, checkin_id):
    checkin_tipo = request.GET.get('checkin_tipo')
    if checkin_tipo == 'individual':
        checkin = get_object_or_404(CheckinIndividual, id=checkin_id)
    elif checkin_tipo == 'empresa':
        checkin = get_object_or_404(CheckinEmpresa, id=checkin_id)
    else:
        return JsonResponse({'error': 'Tipo de check-in inválido'}, status=400)

    hospede = checkin.hospede_principal
    data = {
        'checkin': {
            'data_checkin': checkin.data_checkin,
            'data_checkout': checkin.data_checkout,
            'diaria': checkin.diaria,
            'num_dias': checkin.num_dias,
            'companhia': checkin.companhia,
            'motivo_viagem': checkin.motivo_viagem,
            'acompanhantes': checkin.acompanhantes,
        },
        'hospede': {
            'nome_completo': hospede.nome_completo,
            'cpf': hospede.cpf,
            'email': hospede.email,
            'telefone': hospede.telefone,
            'endereco': hospede.endereco,
            'tipo_cliente': hospede.tipo_cliente,
            'empresa': hospede.empresa.nome_empresa if hospede.empresa else None,
        }
    }
    return JsonResponse(data)


