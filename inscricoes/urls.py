from django.urls import path, re_path
from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'inscricoes'

urlpatterns = [
    path('api/atividades', views.AtividadesAPI.as_view(), name="api-atividades"),
    path('criar', views.CriarInscricao.as_view(),
         name='criar-inscricao'),
    path('<int:pk>/pdf', views.InscricaoPDF,
         name='inscricao-pdf'),
    path('minhasinscricoes', views.MinhasInscricoes.as_view(),
         name='consultar-inscricoes-participante'),
    path('inscricoesdepartamento', views.InscricoesUO.as_view(),
         name='consultar-inscricoes-coordenador'),
    path('inscricoesadmin', views.InscricoesAdmin.as_view(),
         name='consultar-inscricoes-admin'),
    path('<int:pk>', views.ConsultarInscricao.as_view(),
         name='consultar-inscricao'),
    path('<int:pk>/<int:step>', views.ConsultarInscricao.as_view(),
         name='consultar-inscricao'),
    path('alterar/<int:pk>', views.ConsultarInscricao.as_view(), {'alterar': True},
         'alterar-inscricao'),
    path('alterar/<int:pk>/<int:step>', views.ConsultarInscricao.as_view(), {'alterar': True},
         'alterar-inscricao'),
    path('apagar/<int:pk>', views.ApagarInscricao,
         name='apagar-inscricao'),
    path('estatisticas', views.estatisticas,
         name='estatisticas'),
    path('estatisticas/<int:diaabertoid>', views.estatisticas,
         name='estatisticas'),
]
