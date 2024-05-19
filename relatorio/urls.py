from django.urls import path
from . import views

app_name = 'relatorios'
urlpatterns = [
    path('relatorio/Transporte', views.relatorio_Transporte, name='produzirRelatorioTransporte'),
    path('relatorio/pdf/<int:diaabertoid>', views.InscricaoPDF, name='inscricao-pdf'),

]