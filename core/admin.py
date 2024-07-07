from django.contrib import admin
from .models import Quarto, Hospede, Empresa, CheckinIndividual, CheckinEmpresa, Checkout, Reserva, Financeira

admin.site.register(Quarto)
admin.site.register(Hospede)
admin.site.register(Empresa)
admin.site.register(CheckinIndividual)
admin.site.register(CheckinEmpresa)
admin.site.register(Checkout)
admin.site.register(Reserva)
admin.site.register(Financeira)
