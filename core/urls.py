from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('checkin/', views.checkin_view, name='checkin'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('reserva/', views.reserva_view, name='reserva'),
    path('quarto/<int:id>/', views.quarto_detalhes, name='quarto_detalhes'),
    path('financeiro/', views.financeiro_view, name='financeiro'),
    path('incluir_hospede/', views.incluir_hospede_view, name='incluir_hospede_view'),
    path('gerenciar_hospedes/', views.gerenciar_hospedes_view, name='gerenciar_hospedes_view'),
    path('editar_hospede/<int:pk>/', views.editar_hospede_view, name='editar_hospede_view'),
    path('excluir_hospede/<int:pk>/', views.excluir_hospede_view, name='excluir_hospede_view'),
    path('incluir_empresa/', views.incluir_empresa_view, name='incluir_empresa_view'),
    path('gerenciar_empresas/', views.gerenciar_empresas_view, name='gerenciar_empresas_view'),
    path('editar_empresa/<int:pk>/', views.editar_empresa_view, name='editar_empresa_view'),
    path('excluir_empresa/<int:pk>/', views.excluir_empresa_view, name='excluir_empresa_view'),
    path('search_hospede/', views.search_hospede, name='search_hospede'),
    path('search_empresa/', views.search_empresa, name='search_empresa'),
    path('checkin_details/', views.get_checkin_details, name='checkin_details'),
]

