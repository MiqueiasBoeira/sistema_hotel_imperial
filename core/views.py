from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quarto, Hospede, Checkin, Empresa, Checkout, Financeira, Reserva
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import CheckinForm, HospedeForm, EmpresaForm, FinanceiroForm
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
    quartos_livres = Quarto.objects.filter(estado='livre')  # Filtra apenas quartos livres

    if request.method == 'POST':
        form = CheckinForm(request.POST)
        tipo_hospede = request.POST.get('tipo_hospede')

        if form.is_valid():
            checkin = form.save(commit=False)

            if tipo_hospede == 'individual':
                hospede_id = request.POST.get('selected_hospede_id')
                if not hospede_id:
                    form.add_error('selected_hospede_id', 'Selecione um hóspede principal')
                else:
                    hospede_principal = get_object_or_404(Hospede, id=hospede_id)
                    checkin.hospede_principal = hospede_principal

                    hospedes_secundarios = request.POST.getlist('hospede_secundario')
                    checkin.save()
                    checkin.hospedes_secundarios.set(hospedes_secundarios)

            elif tipo_hospede == 'empresa':
                empresa_id = request.POST.get('selected_empresa_id')
                if not empresa_id:
                    form.add_error('selected_empresa_id', 'Selecione uma empresa')
                else:
                    empresa = get_object_or_404(Empresa, id=empresa_id)
                    checkin.empresa = empresa

                    hospedes_empresariais = request.POST.getlist('hospede_empresa')
                    checkin.save()
                    checkin.hospedes_secundarios.set(hospedes_empresariais)

            acompanhantes = form.cleaned_data['acompanhantes']
            checkin.acompanhantes = acompanhantes

            quarto_id = form.cleaned_data['quarto'].id
            quarto = get_object_or_404(Quarto, id=quarto_id)

            checkin.save()
            quarto.estado = 'ocupado'
            quarto.checkin = checkin  # Associa o check-in ao quarto
            quarto.hospede = checkin.hospede_principal  # Atualiza o hóspede do quarto
            quarto.save()
            return redirect('pagina_inicial')
    else:
        form = CheckinForm()

    return render(request, 'core/checkin.html',
                  {'form': form, 'hospedes': hospedes, 'empresas': empresas, 'quartos': quartos_livres})


@login_required
def search_hospede(request):
    query = request.GET.get('q')
    hospedes = Hospede.objects.filter(nome_completo__icontains=query) | Hospede.objects.filter(cpf__icontains=query)
    results = [{'id': hospede.id, 'nome_completo': hospede.nome_completo, 'cpf': hospede.cpf} for hospede in hospedes]
    return JsonResponse(results, safe=False)



@login_required
def search_empresa(request):
    query = request.GET.get('q')
    empresas = Empresa.objects.filter(nome_empresa__icontains=query) | Empresa.objects.filter(cnpj__icontains=query)
    results = [{'id': empresa.id, 'nome_empresa': empresa.nome_empresa, 'cnpj': empresa.cnpj} for empresa in empresas]
    return JsonResponse(results, safe=False)


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
    checkins_ativos = Checkin.objects.filter(quarto__estado='ocupado').exclude(id__in=Checkout.objects.values('checkin_id'))

    if request.method == 'POST':
        checkin_id = request.POST['checkin_id']
        consumo = request.POST['consumo']
        observacoes = request.POST['observacoes']
        metodo_pagamento = request.POST['metodo_pagamento']
        total_pago = request.POST['total_pago']
        data_checkout = request.POST['data_checkout']

        checkin = get_object_or_404(Checkin, id=checkin_id)

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

    return render(request, 'core/checkout.html', {'checkins': checkins_ativos})

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
    checkin = get_object_or_404(Checkin, id=checkin_id)
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

