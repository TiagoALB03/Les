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
    path('almoco_pdf/<int:diaabertoid>', views.pdfalmocos, name='almoco_pdf'),
    path('relatorio_almoco_excel/<int:diaabertoid>', views.relatorio_almoco_excel, name='relatorio_almoco_excel'),
    path('relatorio_almoço', views.relatorio_almoco,name='relatorio_almoço'),
    path('estatisticasAno', views.estatisticasano, name='ano'),
    path('estatisticasAlmoco/<int:diaabertoid>', views.estatisticasAlmocos,
         name='estatisticasAlmocos'),
    path('exportarcsv/<int:diaabertoid>', views.exportarcsv, name='exportarcsvAlmoco'),
    path('inscricao_escolha', views.inscricao_escolha,
         name='inscricao_escolha'),
    path('criar_ultimaHora', views.CriarUltimaHora.as_view(),
         name='criar-inscricao_ultimaHora'),
    path('<int:inscricao_id>/presença', views.presençaInscricao,
         name='presença-inscricao'),
]
