from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('login/', views.login_view, name='login'),
    path('checkin/', views.checkin_view, name='checkin'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('reserva/', views.reserva_view, name='reserva'),
    path('quarto/<int:quarto_id>/', views.quarto_detalhes, name='quarto_detalhes'),
    path('financas/', views.financas_view, name='financas'),
    # Adicione outras rotas conforme necessário
]
