import csv

from django.db.models import OuterRef, Exists, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

import questionario
from configuracao.forms import TemaForm
from utilizadores.views import user_check
from .filters import QuestionarioFilter, TemaPergFilter, TipoRespostaFilter
from .forms import *
from .models import *
from configuracao.models import *
from utilizadores.models import *
from inscricoes.models import Inscricao, Inscricaosessao, Inscricaotransporte
from atividades.models import Tema, Atividade
from datetime import datetime, timezone, date, time
from _datetime import timedelta
from utilizadores.views import user_check
from configuracao.tables import CursoTable, DepartamentoTable, DiaAbertoTable, EdificioTable, MenuTable, TemaTable, \
    TransporteTable, UOTable
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters.views import FilterView
from configuracao.filters import CursoFilter, DepartamentoFilter, DiaAbertoFilter, EdificioFilter, MenuFilter, \
    TemaFilter, TransporteFilter, UOFilter
from .tables import QuestionarioTable, TemaPergTable, TipoRespostaTable, DiaabertoTable
import csv
from django_tables2 import RequestConfig


# Create your views here.
class consultar_questionarios(SingleTableMixin, FilterView):
    table_class = QuestionarioTable
    template_name = 'questionario/questionarioAdmin.html'
    filterset_class = QuestionarioFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["facs"] = list(map(lambda x: (x.id, x.estado), EstadosQuest.objects.all()))
        return context


def criarquestionario(request, questionario_id=None):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')

    questionario = Questionario()
    if questionario_id is not None:
        questionario = Questionario.objects.get(id=questionario_id)
        # questionarioForms = questionarioFormSet(queryset=Questionario.objects.filter(id=questionario.id))
        # allowMore, allowDelete = False, False
    questionarioForm = QuestionarioForm(instance=questionario)

    flagError = False
    flagTituloEmpty = False
    flagDateEmpty = False

    if request.method == 'POST':
        questionarioForm = QuestionarioForm(request.POST, request.FILES, instance=questionario)
        if questionarioForm.is_valid():
            questionario = questionarioForm.save(commit=False)
            # if questionario.dateid is not None:
            #     print("passaste pelo date")
            # if Diaaberto.objects.get(ano=questionario.dateid.ano).questionarioid is None:
            if questionario.titulo is not None and questionario.dateid is not None:
                print("Entraste no questionario")
                questionario.estadoquestid = EstadosQuest.objects.get(id=2)
                questionario.save()
                # diaaberto = Diaaberto.objects.get(ano=questionario.dateid.ano)
                # diaaberto.questionarioid = questionario
                # diaaberto.save()
                return redirect('questionarios:criar-perguntas', questionario_id=questionario.id)
            else:
                flagTituloEmpty = True
                print(flagTituloEmpty)
                # else:
                #     flagError = True
            # else:
            #     flagDateEmpty = True
            #     print(flagDateEmpty)

    return render(request=request,
                  template_name='questionario/criarQuestionario.html',
                  context={'form': questionarioForm,
                           'flagError': flagError,
                           'flagTituloEmpty': flagTituloEmpty,
                           'flagDateEmpty': flagDateEmpty})


# pode ter problemas por já não existir o ano associado ao questionário
def configurarQuestionario(request, questionario_id=None):  #server para alterar alguma informação no questionario
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')

    questionarioFormSet = modelformset_factory(model=Questionario, exclude=['id'], widgets={
        'titulo': TextInput(attrs={'class': 'input'}),
        'dateid': Select(attrs={'class': 'input'}),
        'estadoquestid': Select(attrs={'class': 'input'}),
    }, extra=0, min_num=1, can_delete=True)
    questionarioForms = questionarioFormSet(queryset=Questionario.objects.none())
    questionario = Questionario()

    if questionario_id is not None:
        questionario = Questionario.objects.get(id=questionario_id)
        questionarioForms = questionarioFormSet(queryset=Questionario.objects.filter(id=questionario.id))
        allowMore, allowDelete = False, False

    if (request.method == 'POST'):
        questionarioForms = questionarioFormSet(request.POST)
        if questionarioForms.is_valid():
            questionarioForms.save()
            return redirect('questionarios:consultar-questionarios-admin')

    return render(request=request,
                  template_name='questionario/arquivarQuestionario.html',
                  context={'form': questionarioForms,
                           'allowMore': allowMore,
                           'allowDelete': allowDelete,
                           })


def arquivarQuestionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')

    questionarioAAlterar = Questionario.objects.get(id=questionario_id)
    questionarioAAlterar.estadoquestid = EstadosQuest.objects.get(id=1)
    questionarioAAlterar.save()
    return redirect('questionarios:consultar-questionarios-admin')


def associarAnoQuestionario(request, diaaberto_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')

    # questionario = Questionario.objects.get(id=questionario_id)

    # questionarioForm = Questionario2Form(instance=questionario)
    tabelaDiaAberto = DiaabertoTable(Diaaberto.objects.all())
    RequestConfig(request).configure(tabelaDiaAberto)
    flagError = False

    if request.method == 'POST':
        quest = Questionario2Form(request.POST)
        if quest.is_valid():
            questionario_selecionado = quest.cleaned_data['questionario']
            diaaberto = Diaaberto.objects.get(id=diaaberto_id)
            diaaberto.questionarioid = questionario_selecionado
            diaaberto.save()
            print(questionario_selecionado)
            return redirect('configuracao:diasAbertos')
            # if Diaaberto.objects.get(ano=questionario.dateid.ano).questionarioid is None:
            #     questionario_copia = Questionario.objects.create(titulo=questionario.titulo,
            #                                                      dateid=questionario.dateid,
            #                                                      estadoquestid=EstadosQuest.objects.get(id=2))
            #
            #     perguntas_originais = Pergunta.objects.filter(questionarioid=questionario)
            #     for pergunta in perguntas_originais:
            #         pergunta_copia = Pergunta.objects.create(
            #             pergunta=pergunta.pergunta,
            #             questionarioid=questionario_copia,
            #             temaid=pergunta.temaid,
            #             tiporespostaid=pergunta.tiporespostaid
            #         )
            #
            #     diaaberto = Diaaberto.objects.get(ano=questionario_copia.dateid.ano)
            #     diaaberto.questionarioid = questionario_copia
            #     diaaberto.save()
            #     return redirect('questionarios:consultar-questionarios-admin')
            # else:
            #     flagError = True
    else:
        quest = Questionario2Form()
    # 'form': questionarioForm,
    return render(request=request,
                  template_name='questionario/alterarAno.html',
                  context={
                      'quest': quest,
                      # 'questionario': questionario,
                      'flagError': flagError,
                      'diaabertotable': tabelaDiaAberto})


def criarperguntas(request, questionario_id):
    global pergunta
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')
    questionario = Questionario(id=questionario_id)

    perguntaFormSet = modelformset_factory(model=Pergunta, exclude=['id', 'questionarioid'],
                                           widgets={
                                               'pergunta': TextInput(attrs={'class': 'input'}),
                                               'temaid': Select(attrs={'class': 'input'}),
                                               'tiporespostaid': Select(attrs={'class': 'input'}),
                                           }, extra=0, min_num=1, can_delete=True)

    pergunta_form_set = perguntaFormSet(queryset=Pergunta.objects.none())

    # pergunta = Pergunta()
    allowMore = True
    allowDelete = True

    if request.method == 'POST':
        pergunta_form_set = perguntaFormSet(request.POST)
        if pergunta_form_set.is_valid():
            objectPerg = pergunta_form_set.save(commit=False)
            flag = False
            for obj in objectPerg:
                for perg in Pergunta.objects.all():
                    print("Pergunta do formulário: " + obj.pergunta)
                    print("Pergunta da base de dados: " + perg.pergunta)
                    if obj.pergunta == perg.pergunta:
                        flag = True
                        pergunta = Pergunta.objects.get(id=perg.id)

                if not flag:
                    obj.save()
                    pergunta = Pergunta.objects.get(id=obj.id)
                    pergquest = PergQuest.objects.create(perguntaid=pergunta,
                                                         questionarioid=questionario)
                else:
                    pergquest = PergQuest.objects.create(perguntaid=pergunta,
                                                         questionarioid=questionario)

            return redirect('questionarios:consultar-questionarios-admin')
    return render(request=request,
                  template_name='questionario/criarPerguntas.html',
                  context={'form': pergunta_form_set,
                           'questionarioID': questionario_id,
                           'allowMore': allowMore,
                           'allowDelete': allowDelete})


def newPergRow(request):
    value = int(request.POST.get('extra'))
    data = {
        'form_pergunta': "form-" + str(value - 1) + "-pergunta",
        'form_temaid': "form-" + str(value - 1) + "-temaid",
        'form_tiporespostaid': "form-" + str(value - 1) + "-tiporespostaid",
        'form_id': 'form-' + str(value - 1) + '-id',
        'tipos': TipoResposta.objects.all(),
        'options': TemaPerg.objects.all(),
    }
    print(data)
    return render(request=request, template_name='questionario/questionarioPerguntasRow.html', context=data)


class consultartema(SingleTableMixin, FilterView):
    table_class = TemaPergTable
    template_name = 'questionario/listarTema.html'
    filterset_class = TemaPergFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[Administrador])
        if not user_check_var.get('exists'): return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


def criarTema(request):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    tema = TemaPerg()
    flag = 0
    temaExist = False

    temaForm = TemaFormPerg(instance=tema)
    if request.method == 'POST':
        temaForm = TemaFormPerg(data=request.POST, instance=tema)
        if temaForm.is_valid():
            tema = temaForm.save(commit=False)

            for obj in TemaPerg.objects.all():
                if obj.tema == tema.tema:
                    flag = 1
                    temaExist = True
                    break

            if flag == 0:
                tema = temaForm.save()
                return redirect('questionarios:consultar-tema')

    return render(request=request,
                  template_name='questionario/criarTema.html',
                  context={'form': temaForm,
                           'temaExist': temaExist})


class consultartiporesposta(SingleTableMixin, FilterView):
    table_class = TipoRespostaTable
    template_name = 'questionario/listarTipoResposta.html'
    filterset_class = TipoRespostaFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)


def criarTipoRespost(request):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    tiporesposta = TipoResposta()

    tipoespostaForm = TipoRespostaForm(instance=tiporesposta)
    if request.method == 'POST':
        tipoespostaForm = TipoRespostaForm(data=request.POST, instance=tiporesposta)
        if tipoespostaForm.is_valid():
            tema = tipoespostaForm.save()
            return redirect('questionarios:consultar-tipo-resposta')

    return render(request=request,
                  template_name='questionario/criarTipoResposta.html',
                  context={'form': tipoespostaForm})


def estatisticas(request, diaabertoid=None):
    """ View que mostra as estatísticas do Dia Aberto """
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    if diaabertoid is None:
        try:
            return render(request, 'questionario/estatisticaVazia.html', {
                'diasabertos': Diaaberto.objects.all()
            })
        except:
            return redirect('utilizadores:mensagem', 18)

    diaaberto = get_object_or_404(Diaaberto, id=diaabertoid)
    numdays = int((diaaberto.datadiaabertofim -
                   diaaberto.datadiaabertoinicio).days) + 1
    dias = [(diaaberto.datadiaabertoinicio + timedelta(days=x)
             ).strftime("%d/%m/%Y") for x in range(numdays)]

    if request.method == 'GET':
        subtemaid = request.GET.get('atividade_id')
        print("Esta certo subtema ->", subtemaid)

    # perguntaid__questionarioid__dateid
    respostas = Resposta.objects.filter(perguntaID__pergquest__questionarioid__dateid=diaaberto)
    return render(request, 'questionario/estatisticas.html', {
        'diaaberto': diaaberto,
        'diasabertos': Diaaberto.objects.all(),
        'departamentos': Departamento.objects.filter(
            Exists(
                Atividade.objects.filter(
                    professoruniversitarioutilizadorid__departamento__id=OuterRef(
                        'id'),
                    diaabertoid__id=diaabertoid,
                    estado="Aceite",
                )
            )
        ),
        'dias': dias,
        # 'meios': TransporteGeral.objects.all(),
        'meios': TransporteGeral.objects.get(id=2),
        # 'roteiros': Roteiro.objects.filter(diaabertoid=diaaberto.id),
        'respostas': respostas,
        'subtemaid': subtemaid,
        'counter2': respostas.filter(resposta="2").count(),
        'counter3': respostas.filter(resposta="3").count(),
        'counter4': respostas.filter(resposta="4").count(),
        'counter5': respostas.filter(resposta="5").count(),
        'sub': subtemaid,
        'subtema': 2,
    })


def getRespostas(request):
    if request.method == 'POST':
        counter_str = request.POST.get('subtema')  # Default value if not provided
        # print(counter_str)
        diaID = request.POST.get('diaaberto')
        try:
            counter = int(counter_str)
            # print("CONTADOR", counter)
            if counter != -1:
                respostas = Resposta.objects.filter(subtemaid=counter)
            else:
                respostas = Resposta.objects.filter(perguntaID__questionarioid__dateid=diaID)
            # print(respostas.count())
            return JsonResponse({'subtema': counter,
                                 'respostas': list(respostas.values())})
        except ValueError:
            print("ERROR")
            # Handle the case where counter is not a valid integer
            counter = 0  # Set a default value or handle the error as appropriate
            return JsonResponse({'subtema': counter,
                                 'respostas': []})


def exportarCSV(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Qestionario', 'Ano', 'Estado'])
    for questionario in Questionario.objects.all().values_list('id', 'titulo', 'dateid', 'estadoquestid'):
        writer.writerow(questionario)
    writer.writerow([])

    writer.writerow(['id', 'Pergunta', 'QuestionarioID', 'Tema', 'Tipo de Resposta'])
    for pergunta in Pergunta.objects.all().values_list('pergunta', 'questionarioid', 'temaid', 'tiporespostaid'):
        writer.writerow(pergunta)

    writer.writerow([])
    writer.writerow(['PerguntaID', 'Resposta', 'Subtema'])

    for resposta in Resposta.objects.all().values_list('perguntaID', 'resposta', 'subtemaid'):
        writer.writerow(resposta)

    response['Content-Disposition'] = 'attachment; filename="Respostas.csv"'

    return response
