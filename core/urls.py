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
    # Adicione outras rotas conforme necessário
]
