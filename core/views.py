import logging
import locale
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateformat import format as date_format
from .models import Quarto, Hospede, CheckinIndividual, CheckinEmpresa, Empresa, Checkout, Financeira, Reserva
from .forms import CheckinIndividualForm, CheckinEmpresaForm, HospedeForm, EmpresaForm, FinanceiroForm, CheckoutForm


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
    quartos = Quarto.objects.select_related('checkin_individual__hospede_principal', 'checkin_empresa__hospede_principal', 'checkin_empresa__empresa').all()
    context = {
        'quartos': quartos
    }
    return render(request, 'core/pagina_inicial.html', context)

@login_required
def quarto_detalhes(request, id):
    quarto = get_object_or_404(Quarto, id=id)
    reservas = quarto.reservas.filter(status='ativo')

    context = {
        'quarto': quarto,
        'reservas': reservas
    }
    return render(request, 'core/quarto_detalhes.html', context)


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

logger = logging.getLogger(__name__)


@login_required
def checkin_view(request):
    hospedes = Hospede.objects.all()
    empresas = Empresa.objects.all()
    quartos_livres = Quarto.objects.filter(estado='livre')

    if request.method == 'POST':
        tipo_hospede = request.POST.get('tipo_hospede')

        if tipo_hospede == 'individual':
            form_individual = CheckinIndividualForm(request.POST)
            if form_individual.is_valid():
                checkin = form_individual.save(commit=False)
                hospede_principal_id = request.POST.get('selected_hospede_id')
                hospede_principal = get_object_or_404(Hospede, id=hospede_principal_id)
                checkin.hospede_principal = hospede_principal
                checkin.save()

                # Obter IDs dos hóspedes secundários
                hospedes_secundarios_ids = request.POST.getlist('hospedes_secundarios_ids')

                # Filtrar IDs não vazios e remover o ID do hóspede principal
                hospedes_secundarios_ids = [id for id in hospedes_secundarios_ids if id and id != str(hospede_principal.id)]

                hospedes_secundarios = Hospede.objects.filter(id__in=hospedes_secundarios_ids)
                checkin.hospedes_secundarios.set(hospedes_secundarios)

                # Atualiza o estado do quarto
                quarto = checkin.quarto
                quarto.estado = 'ocupado'
                quarto.checkin_individual = checkin
                quarto.tipo_checkin = 'individual'
                quarto.save()

                messages.success(request, 'Check-in realizado com sucesso.')
                return redirect('pagina_inicial')
            else:
                messages.error(request, 'Erro ao realizar check-in individual. Verifique os dados e tente novamente.')

        elif tipo_hospede == 'empresa':
            form_empresa = CheckinEmpresaForm(request.POST)
            if form_empresa.is_valid():
                checkin = form_empresa.save(commit=False)
                empresa = get_object_or_404(Empresa, id=request.POST.get('selected_empresa_id'))
                hospede_principal = get_object_or_404(Hospede, id=request.POST.get('selected_hospede_empresa_id'))
                checkin.empresa = empresa
                checkin.hospede_principal = hospede_principal
                checkin.save()

                # Obter IDs dos hóspedes secundários
                hospedes_secundarios_ids = request.POST.getlist('hospedes_secundarios_ids')

                # Filtrar IDs não vazios e remover o ID do hóspede principal
                hospedes_secundarios_ids = [id for id in hospedes_secundarios_ids if id and id != str(hospede_principal.id)]

                hospedes_secundarios = Hospede.objects.filter(id__in=hospedes_secundarios_ids)
                checkin.hospedes_secundarios.set(hospedes_secundarios)

                # Atualiza o estado do quarto
                quarto = checkin.quarto
                quarto.estado = 'ocupado'
                quarto.checkin_empresa = checkin
                quarto.tipo_checkin = 'empresa'
                quarto.save()

                messages.success(request, 'Check-in empresarial realizado com sucesso.')
                return redirect('pagina_inicial')
            else:
                messages.error(request, 'Erro ao realizar check-in empresarial. Verifique os dados e tente novamente.')

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
        checkin_id = request.POST.get('checkin_id')
        checkin_tipo = request.POST.get('checkin_tipo')
        form = CheckoutForm(request.POST)

        if form.is_valid():
            checkout = form.save(commit=False)
            if checkin_tipo == 'individual':
                checkin = get_object_or_404(CheckinIndividual, id=checkin_id)
                checkout.checkin_individual = checkin
            elif checkin_tipo == 'empresa':
                checkin = get_object_or_404(CheckinEmpresa, id=checkin_id)
                checkout.checkin_empresa = checkin

            checkout.save()

            # Atualiza o estado do quarto
            quarto = checkin.quarto
            quarto.estado = 'livre'
            quarto.save()

            # Adiciona o registro financeiro
            Financeira.objects.create(
                tipo='receita',
                descricao=f'Checkout do quarto {checkin.quarto.numero_quarto}',
                valor=checkout.total_pago,
                data=checkout.data_checkout
            )

            messages.success(request, 'Check-out realizado com sucesso.')
            return redirect('pagina_inicial')
        else:
            messages.error(request, 'Erro ao realizar check-out. Verifique os dados e tente novamente.')

    return render(request, 'core/checkout.html', {
        'checkins_individuais': checkins_individuais_ativos,
        'checkins_empresas': checkins_empresas_ativos,
        'form': CheckoutForm()
    })

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

        messages.success(request, 'Reserva realizada com sucesso.')
        return redirect('reserva')

    hospedes = Hospede.objects.all()
    quartos = Quarto.objects.all()
    return render(request, 'core/reserva.html', {'hospedes': hospedes, 'quartos': quartos})


# Defina a localidade para exibir os valores corretamente
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
@login_required
@permission_required('core.view_financeira', raise_exception=True)
def financeiro_view(request):
    form = FinanceiroForm()
    lancamentos = Financeira.objects.none()
    saldo = None

    if request.method == 'POST' and 'calcular_saldo' in request.POST:
        form = FinanceiroForm(request.POST)
        if form.is_valid():
            data_inicial = form.cleaned_data['data_inicial']
            data_final = form.cleaned_data['data_final']
            if data_inicial and data_final:
                lancamentos = Financeira.objects.filter(data__range=[data_inicial, data_final])
            else:
                lancamentos = Financeira.objects.all()
            saldo = calcular_saldo(lancamentos)

    elif request.method == 'POST' and 'tipo' in request.POST:
        tipo = request.POST['tipo']
        descricao = request.POST['descricao']
        valor = request.POST['valor']
        data = request.POST['data']
        Financeira.objects.create(tipo=tipo, descricao=descricao, valor=valor, data=data)
        return redirect('financeiro')

    # Formatar os valores monetários e datas
    lancamentos_formatados = []
    for lancamento in lancamentos:
        lancamentos_formatados.append({
            'data': date_format(lancamento.data, 'd/m/Y'),
            'tipo': lancamento.tipo,
            'descricao': lancamento.descricao,
            'valor': f"R$ {lancamento.valor:,.2f}".replace('.', ',')
        })

    saldo_formatado = f"R$ {saldo:,.2f}".replace('.', ',') if saldo is not None else None

    return render(request, 'core/financas.html', {'form': form, 'lancamentos': lancamentos_formatados, 'saldo': saldo_formatado})

def calcular_saldo(lancamentos):
    saldo = 0
    for lancamento in lancamentos:
        if lancamento.tipo == 'receita':
            saldo += lancamento.valor
        else:
            saldo -= lancamento.valor
    return saldo


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


