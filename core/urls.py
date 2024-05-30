from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('login/', views.login_view, name='login'),
    path('checkin/', views.checkin_view, name='checkin'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('reserva/', views.reserva_view, name='reserva'),
    path('quarto/<int:quarto_id>/', views.quarto_detalhes, name='quarto_detalhes'),
    path('financas/', views.financas_view, name='financas'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('hospedes/incluir/', views.incluir_hospede_view, name='incluir_hospede_view'),
    path('hospedes/', views.gerenciar_hospedes_view, name='gerenciar_hospedes_view'),
    path('hospedes/editar/<int:pk>/', views.editar_hospede_view, name='editar_hospede_view'),
    path('hospedes/excluir/<int:pk>/', views.excluir_hospede_view, name='excluir_hospede_view'),
    # Adicione outras rotas conforme necessário
]
