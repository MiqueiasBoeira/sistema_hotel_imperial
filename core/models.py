from django.db import models

class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome_empresa

class Hospede(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_completo

class Quarto(models.Model):
    numero_quarto = models.CharField(max_length=10)
    estado = models.CharField(max_length=10, choices=[('livre', 'Livre'), ('ocupado', 'Ocupado'), ('reservado', 'Reservado')])
    hospede = models.ForeignKey(Hospede, null=True, blank=True, on_delete=models.SET_NULL, related_name='quartos')
    checkin_individual = models.OneToOneField('CheckinIndividual', null=True, blank=True, on_delete=models.SET_NULL, related_name='quarto_checkin_individual')
    checkin_empresa = models.OneToOneField('CheckinEmpresa', null=True, blank=True, on_delete=models.SET_NULL, related_name='quarto_checkin_empresa')
    tipo_checkin = models.CharField(max_length=10, choices=[('individual', 'Individual'), ('empresa', 'Empresa')], null=True, blank=True)

    def __str__(self):
        return self.numero_quarto

class CheckinIndividual(models.Model):
    hospede_principal = models.ForeignKey(Hospede, on_delete=models.CASCADE, related_name='checkins_individual')
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='checkins_individual')
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    diaria = models.DecimalField(max_digits=10, decimal_places=2)
    num_dias = models.IntegerField()
    companhia = models.CharField(max_length=255, null=True, blank=True)
    motivo_viagem = models.CharField(max_length=255)
    acompanhantes = models.TextField(null=True, blank=True)  # Lista de nomes de acompanhantes
    hospedes_secundarios = models.ManyToManyField(Hospede, related_name='checkins_secundarios_individual', blank=True)

    def __str__(self):
        return f'{self.hospede_principal.nome_completo} - {self.quarto.numero_quarto}'

class CheckinEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='checkins_empresa')
    hospede_principal = models.ForeignKey(Hospede, on_delete=models.CASCADE, related_name='checkins_empresa_principal')
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='checkins_empresa')
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    diaria = models.DecimalField(max_digits=10, decimal_places=2)
    num_dias = models.IntegerField()
    companhia = models.CharField(max_length=255, null=True, blank=True)
    motivo_viagem = models.CharField(max_length=255)
    acompanhantes = models.TextField(null=True, blank=True)  # Lista de nomes de acompanhantes
    hospedes_secundarios = models.ManyToManyField(Hospede, related_name='checkins_secundarios_empresa', blank=True)

    def __str__(self):
        return f'{self.empresa.nome_empresa} - {self.quarto.numero_quarto}'

class Checkout(models.Model):
    checkin_individual = models.ForeignKey(CheckinIndividual, null=True, blank=True, on_delete=models.SET_NULL, related_name='checkouts')
    checkin_empresa = models.ForeignKey(CheckinEmpresa, null=True, blank=True, on_delete=models.SET_NULL, related_name='checkouts')
    data_checkout = models.DateField()
    consumo = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(null=True, blank=True)
    metodo_pagamento = models.CharField(max_length=50)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.checkin_individual:
            return f'Checkout Individual - {self.checkin_individual.hospede_principal.nome_completo}'
        elif self.checkin_empresa:
            return f'Checkout Empresa - {self.checkin_empresa.empresa.nome_empresa}'
        return 'Checkout'

class Financeira(models.Model):
    tipo = models.CharField(max_length=10, choices=[('receita', 'Receita'), ('despesa', 'Despesa')])
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f'{self.tipo} - {self.descricao}'

class Reserva(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='reservas')
    hospede = models.ForeignKey(Hospede, null=True, blank=True, on_delete=models.SET_NULL, related_name='reservas')
    nome_hospede = models.CharField(max_length=255)
    contato_hospede = models.CharField(max_length=20)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('cancelado', 'Cancelado')], default='ativo')

    def __str__(self):
        return f'Reserva {self.quarto.numero_quarto} - {self.nome_hospede}'
