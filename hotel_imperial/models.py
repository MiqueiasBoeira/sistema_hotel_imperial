from django.db import models

class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self):
        return self.nome_empresa


class Hospede(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    tipo_cliente = models.CharField(max_length=10, choices=[('individual', 'Individual'), ('empresa', 'Empresa')])
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_completo



class Quarto(models.Model):
    numero_quarto = models.CharField(max_length=10)
    estado = models.CharField(max_length=10, choices=[('livre', 'Livre'), ('ocupado', 'Ocupado'), ('reservado', 'Reservado')])

    def __str__(self):
        return self.numero_quarto


class Checkin(models.Model):
    hospede = models.ForeignKey(Hospede, on_delete=models.CASCADE)
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    data_checkin = models.DateField()
    diaria = models.DecimalField(max_digits=10, decimal_places=2)
    num_dias = models.IntegerField()
    companhia = models.CharField(max_length=255, null=True, blank=True)
    motivo_viagem = models.CharField(max_length=255)
    numero_total_hospedes = models.IntegerField()

    def __str__(self):
        return f'{self.hospede.nome_completo} - Quarto {self.quarto.numero_quarto}'


class Checkout(models.Model):
    checkin = models.ForeignKey(Checkin, on_delete=models.CASCADE)
    data_checkout = models.DateField()
    consumo = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(null=True, blank=True)
    metodo_pagamento = models.CharField(max_length=50)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Checkout {self.checkin.id} - Quarto {self.checkin.quarto.numero_quarto}'

class Reserva(models.Model):
    data_inicio = models.DateField()
    data_fim = models.DateField()
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    hospede = models.ForeignKey(Hospede, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Reserva Quarto {self.quarto.numero_quarto}'


class Financeira(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f'{self.tipo.capitalize()} - {self.descricao}'

