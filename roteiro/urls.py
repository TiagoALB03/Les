from django.urls import path
from . import views

app_name = 'roteiros'
urlpatterns = [
    path('roteiros', views.roteiroCoordenador.as_view(), name='roteiroCoordenador'),
    path('consultarRoteiro/<int:roteiro_id>', views.consultarRoteiro, name='consultarRoteiro'),
]