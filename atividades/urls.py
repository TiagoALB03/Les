from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'atividades'

urlpatterns = [
    path('minhasatividades',views.AtividadesProfessor.as_view(),name="minhasAtividades"),
    path('atividadadesUOrganica',views.AtividadesCoordenador.as_view(),name="atividadesUOrganica"),
    path('alteraratividade/<int:id>',views.alterarAtividade,name='alterarAtividade'),
    path('sessao/<int:id>',views.inserirsessao,name='inserirSessao'),
    path('eliminaratividade/<int:id>',views.eliminarAtividade,name='eliminarAtividade'),
    path('eliminarsessao/<int:id>',views.eliminarSessao,name='eliminarSessao'),
    path('proporatividade',views.proporatividade,name='proporAtividade'),
    path('validaratividade/<int:id>/<int:action>',views.validaratividade,name='validarAtividade'),
    path('veredificios',views.veredificios,name="verEdificios"),
    path('versalas',views.versalas,name="verSalas"),
    path('verhorarios',views.verhorarios,name="verHorarios"),
    path('verresumo/<int:id>',views.verresumo,name='verResumo'),
    path('confirmar/<int:id>',views.confirmarResumo,name='confirmarResumo'),
    path('atividadesadmin',views.AtividadesAdmin.as_view(),name="atividadesAdmin"),
    path('verdeps',views.verdeps,name="verDepartamentos"),
    path('veruos',views.verfaculdades,name="verFaculdades"),
]

