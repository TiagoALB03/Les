import csv

from django.db.models import OuterRef, Exists, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

import questionario
from configuracao.forms import TemaForm
from roteiro.models import Roteiro
from utilizadores.views import user_check
from .filters import QuestionarioFilter, TemaPergFilter, TipoRespostaFilter, EstadosFilter
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
from .tables import QuestionarioTable, TemaPergTable, TipoRespostaTable, DiaabertoTable, EstadoTable
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
        context["facs"] = list(map(lambda x: (x.id, x.nome), EstadosQuest.objects.all()))
        return context


def criarquestionario(request, questionario_id=None):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')

    questionario = Questionario()
    if questionario_id is not None:
        questionario = Questionario.objects.get(id=questionario_id)
    questionarioForm = QuestionarioForm(instance=questionario)

    flagError = False
    flagTituloEmpty = False
    flagDateEmpty = False

    if request.method == 'POST':
        questionarioForm = QuestionarioForm(request.POST, request.FILES, instance=questionario)
        if questionarioForm.is_valid():
            questionario = questionarioForm.save(commit=False)
            if questionario.titulo is not None:
                print("Entraste no questionario")
                questionario.estadoquestid = EstadosQuest.objects.get(id=2)
                questionario.save()
                return redirect('questionarios:criar-perguntas', questionario_id=questionario.id)
            else:
                flagTituloEmpty = True
                print(flagTituloEmpty)

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


def responder_questionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')

    questionario = get_object_or_404(Questionario, id=questionario_id)
    pergquest_ids = PergQuest.objects.filter(questionarioid=questionario).values_list('perguntaid', flat=True)
    perguntas = Pergunta.objects.filter(id__in=pergquest_ids).order_by('id')

    if request.method == 'POST':
        for pergunta in perguntas:
            resposta_data = request.POST.get(str(pergunta.id), '')
            resposta, created = Resposta.objects.update_or_create(
                perguntaID=pergunta,
                idcodigo=request.user.codigoquestionario,
                defaults={'resposta': resposta_data}
            )
        return redirect('questionarios:consultar-questionarios-admin')

    return render(request, 'questionario/responderQuestionario.html', {
        'questionario': questionario,
        'perguntas': perguntas
    })


def editar_questionario(request, questionario_id):
    questionario = get_object_or_404(Questionario, id=questionario_id)
    PerguntaFormSet = modelformset_factory(Pergunta, form=PerguntasForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = PerguntaFormSet(request.POST, request.FILES,
                                  queryset=Pergunta.objects.filter(pergquest__questionarioid=questionario))

        if formset.is_valid():
            perguntas = formset.save(commit=False)

            for pergunta in perguntas:
                pergunta.save()  # Salva a pergunta primeiro

                PergQuest.objects.update_or_create(
                    perguntaid=pergunta,
                    defaults={'questionarioid': questionario}
                )

            # Deleta as perguntas marcadas para remoção
            for obj in formset.deleted_objects:
                obj.delete()

            formset.save_m2m()  # Salva as relações ManyToMany, se houver

            return redirect('questionarios:consultar-questionarios-admin')  # Redireciona para a lista de questionários

    else:
        formset = PerguntaFormSet(queryset=Pergunta.objects.filter(pergquest__questionarioid=questionario))

    return render(request, 'questionario/editar_questionario.html', {'formset': formset, 'questionario': questionario})


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
    tiporespostaExist = False
    flag = 0
    tipoespostaForm = TipoRespostaForm(instance=tiporesposta)
    if request.method == 'POST':
        tipoespostaForm = TipoRespostaForm(data=request.POST, instance=tiporesposta)
        if tipoespostaForm.is_valid():
            tiporesposta = tipoespostaForm.save(commit=False)

            for obj in TipoResposta.objects.all():
                if obj.tiporesposta == tiporesposta.tiporesposta:
                    flag = 1
                    tiporespostaExist = True
                    break

            if flag == 0:
                tiporesposta = tipoespostaForm.save()
                return redirect('questionarios:consultar-tipo-resposta')

    return render(request=request,
                  template_name='questionario/criarTipoResposta.html',
                  context={'form': tipoespostaForm,
                           'tiporespostaExist': tiporespostaExist})


def estatisticasTransport(request, diaabertoid=None):
    """ View que mostra as estatísticas do Dia Aberto """
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    if diaabertoid is None:
        try:
            return render(request, 'questionario/estatisticaVaziaTransport.html', {
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

    # perguntaid__questionarioid__dateid   perguntaID__pergquest__questionarioid__dateid
    respostas = Resposta.objects.filter(perguntaID__pergquest__questionarioid=diaaberto.questionarioid)
    return render(request, 'questionario/estatisticasTransport.html', {
        'diaaberto': diaaberto,
        'diasabertos': Diaaberto.objects.all(),
        'departamentos': Departamento.objects.filter(
            Exists(
                Atividade.objects.filter(
                    professoruniversitarioutilizadorid__departamento__id=OuterRef(
                        'id'),
                    diaabertoid__id=diaabertoid,
                    estado__nome="Aceite",
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


def exportarCSVTransporte(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Respostas.csv"'
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['ID', 'Qestionario', 'Estado'])
    for questionario in Questionario.objects.all().values_list('id', 'titulo', 'estadoquestid'):
        writer.writerow(questionario)
    writer.writerow([])

    writer.writerow(['id', 'Pergunta', 'QuestionarioID', 'Tema', 'Tipo de Resposta'])
    for pergunta in Pergunta.objects.all().values_list('pergunta', 'temaid', 'tiporespostaid'):
        writer.writerow(pergunta)

    writer.writerow([])
    writer.writerow(['PerguntaID', 'Resposta', 'Subtema'])

    for resposta in Resposta.objects.all().values_list('perguntaID', 'resposta', 'subtemaid'):
        writer.writerow(resposta)

    # response['Content-Disposition'] = 'attachment; filename="Respostas.csv"'

    return response


class consultar_estados(SingleTableMixin, FilterView):
    table_class = EstadoTable
    template_name = 'questionario/listarEstados.html'
    table_pagination = {
        'per_page': 5
    }
    filterset_class = EstadosFilter

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


def eliminarEstado(request, estados_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    estado = get_object_or_404(EstadosQuest, id=estados_id)
    estado.delete()
    return redirect('questionarios:consultar-estados-admin')


def editarEstado(request, estados_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')
    estadoFormSet = modelformset_factory(model=EstadosQuest, exclude=['id'], widgets={
        'nome': TextInput(attrs={'class': 'input'}),
        'cor': TextInput(
            attrs={'type': 'color', 'class': 'color-picker', 'id': 'colorpicker', 'onchange': 'displayHexColor()'}),
    }, extra=0, min_num=1, can_delete=True)
    estadoForms = estadoFormSet(queryset=EstadosQuest.objects.none())
    estado = EstadosQuest()
    mensagemErro = ''
    if estados_id is not None:
        estado = EstadosQuest.objects.get(id=estados_id)
        estadoForms = estadoFormSet(queryset=EstadosQuest.objects.filter(id=estado.id))
        allowMore, allowDelete = False, False
    if (request.method == 'POST'):
        estadoForms = estadoFormSet(request.POST)
        if estadoForms.is_valid():
            novoEstadoNome = estadoForms.cleaned_data[0]['nome']
            novaCor = estadoForms.cleaned_data[0]['cor']
            flagCor = EstadosQuest.objects.filter(cor=novaCor).exists() and novaCor != estado.cor
            flagNome = EstadosQuest.objects.filter(nome=novoEstadoNome).exists() and novoEstadoNome != estado.nome
            flagQuest = Questionario.objects.filter(
                estadoquestid__nome=estado.nome).exists() and novoEstadoNome != estado.nome
            flagRoteiroNome = Roteiro.objects.filter(
                estado__nome=estado.nome).exists() and novoEstadoNome != estado.nome
            flagAtividadeNome = Atividade.objects.filter(
                estado__nome=estado.nome).exists() and novoEstadoNome != estado.nome

            if flagQuest and flagCor:
                mensagemErro = 'Não podes mudar o nome de um estado que está em uso num questionário.A cor já existe,escolhe outra.'
            elif flagQuest:
                mensagemErro = 'Não podes mudar o nome de um estado que está em uso num questionário.'
            elif flagRoteiroNome and flagCor:
                mensagemErro = 'Não podes mudar o nome de um estado que está em uso num roteiro.A cor já existe,escolhe outra.'
            elif flagRoteiroNome:
                mensagemErro = 'Não podes mudar o nome de um estado que está em uso num roteiro.'
            elif flagAtividadeNome and flagCor:
                mensagemErro = 'Não podes mudar o nome de um estado que está em uso num Atividade.A cor já existe,escolhe outra.'
            elif flagAtividadeNome:
                mensagemErro = 'Não podes mudar o nome de um estado que está em uso numa atividade.'
            elif flagCor and flagNome:
                mensagemErro = 'O estado e a cor já existem. Escolhe outros.'
            elif flagNome:
                mensagemErro = "O estado já existe. Escolhe outro."
            elif flagCor:
                mensagemErro = "A cor já existe. Escolhe outra."
            else:
                estado.cor = novaCor
                estado.nome = novoEstadoNome
                estado.save()
                return redirect('questionarios:consultar-estados-admin')

    return render(request=request,
                  template_name='questionario/editarEstados.html',
                  context={'form': estadoForms,
                           'allowMore': allowMore,
                           'allowDelete': allowDelete,
                           'erroMensagem': mensagemErro,
                           })


def publicarQuestionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    try:
        questionario = Questionario.objects.get(id=questionario_id)
        questionario.estadoquestid = EstadosQuest.objects.get(nome='publicado')
        questionario.save()
        return redirect('questionarios:consultar-questionarios-admin')
    except Questionario.DoesNotExist:
        return HttpResponse("Questionário não encontrado.")
    except EstadosQuest.DoesNotExist:
        return HttpResponse("Estado não encontrado.")


def validarQuestionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    try:
        questionario = Questionario.objects.get(id=questionario_id)
        questionario.estadoquestid = EstadosQuest.objects.get(nome='validado')
        questionario.save()
        return redirect('questionarios:consultar-questionarios-admin')
    except Questionario.DoesNotExist:
        return HttpResponse("Questionário não encontrado.")
    except EstadosQuest.DoesNotExist:
        return HttpResponse("Estado não encontrado.")


def criarEstado(request):
    mensagemErro = ''
    if request.method == 'POST':
        form = EstadoForm(request.POST)
        if form.is_valid():
            flagCor = EstadosQuest.objects.filter(cor=form.cleaned_data['cor']).exists()
            flagNome = EstadosQuest.objects.filter(nome=form.cleaned_data['nome']).exists()
            if flagCor and flagNome:
                mensagemErro = 'O estado e a cor já existem. Escolhe outros.'
            elif flagNome:
                mensagemErro = "O estado já existe. Escolhe outro."
            elif flagCor:
                mensagemErro = "A cor já existe. Escolhe outra."
            else:
                form.save()
                return redirect('questionarios:consultar-estados-admin')
    else:
        form = EstadoForm()

    return render(request, 'questionario/criarEstado.html', {'form': form,
                                                             'erroMensagem': mensagemErro})


def criar_escala_resposta(request):
    if request.method == 'POST':
        form = EscalaRespostaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('questionarios:consultar-tipo-resposta')  # Redirecionar após criar a escala
    else:
        form = EscalaRespostaForm()
    return render(request, 'questionario/criarEscalaResposta.html', {'form': form})


def listar_escala_resposta(request):
    escalas = questionario_escalaresposta.objects.all()
    return render(request, 'questionario/listarEscalaResposta.html', {'escalas': escalas})


def editar_escala_resposta(request, id):
    escala = get_object_or_404(questionario_escalaresposta, id=id)
    form = EscalaRespostaForm(request.POST or None, instance=escala)
    if form.is_valid():
        form.save()
        return redirect('questionarios:listar-escala-resposta')  # Substitua pela sua view de listagem
    return render(request, 'questionario/editarEscalaResposta.html', {'form': form})


def estatisticasAtividadeRoteiro(request, diaabertoid=None):
    """ View que mostra as estatísticas do Dia Aberto """
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    if diaabertoid is None:
        try:
            return render(request, 'questionario/estatisticaVaziaAtividadeRoteiro.html', {
                'diasabertos': Diaaberto.objects.all(),
                'mensagem': ''
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

    respostas = Resposta.objects.all().filter(idcodigo__inscricaoID__inscricao__diaaberto=diaaberto)

    if not respostas.exists():
        try:
            return render(request, 'questionario/estatisticaVaziaAtividadeRoteiro.html', {
                'diasabertos': Diaaberto.objects.all(),
                'mensagem': 'Não existe respostas no dia aberto ',
                'diaaberto': diaaberto,
            })
        except:
            return redirect('utilizadores:mensagem', 18)
    atividades = Atividade.objects.filter(diaabertoid=diaaberto.id)
    roteiros = Roteiro.objects.filter(diaabertoid=diaaberto.id)
    print("rot", roteiros)
    print("ativ", atividades)
    return render(request, 'questionario/estatisticasAtividadeRoteiro.html', {
        'diaaberto': diaaberto,
        'diasabertos': Diaaberto.objects.all(),
        'departamentos': Departamento.objects.filter(
            Exists(
                Atividade.objects.filter(
                    professoruniversitarioutilizadorid__departamento__id=OuterRef(
                        'id'),
                    diaabertoid__id=diaabertoid,
                    estado__nome="Aceite",
                )
            )
        ),
        'dias': dias,
        'meios': Inscricao.MEIO_TRANSPORTE_CHOICES,
        'roteiros': Roteiro.objects.filter(diaabertoid=diaaberto.id),
        'atividades': Atividade.objects.filter(diaabertoid=diaaberto.id),
        'respostas': respostas,
        'respostasRoteiros': respostas,
        'subtemaid': subtemaid,
        'counter2': respostas.filter(resposta="2").count(),
        'counter3': respostas.filter(resposta="3").count(),
        'counter4': respostas.filter(resposta="4").count(),
        'counter5': respostas.filter(resposta="5").count(),
        'sub': subtemaid,
        'subtema': 2,
    })


def getRespostasAtividadeRoteiro(request):
    if request.method == 'POST':
        roteiro = request.POST.get('roteiroID')
        tema = request.POST.get('temaID')
        diaID = request.POST.get('diaaberto')
        print("idDIA", diaID)
        try:
            roteiroID = int(roteiro)
            temaID = int(tema)
            print("ID ROTEIRO", roteiroID)
            print("ID TEMA", temaID)
            print("ID DIA", diaID)
            if roteiroID != -1:
                if temaID == -1:
                    respostas = Resposta.objects.filter(idcodigo__inscricaoID__sessao__roteiro=roteiroID)
                else:
                    respostas = Resposta.objects.filter(idcodigo__inscricaoID__sessao__roteiro=roteiroID,
                                                        subtemaid=temaID)
                atividades = Atividade.objects.filter(roteiro=roteiroID)
            else:
                if temaID == -1:
                    respostas = Resposta.objects.filter(perguntaID__questionarioid__dateid=diaID)
                else:
                    respostas = Resposta.objects.filter(subtemaid=temaID)
                atividades = Atividade.objects.filter(roteiro__diaabertoid=diaID)
            return JsonResponse({'subtema': roteiroID,
                                 'respostas': list(respostas.values()),
                                 'atividades': list(atividades.values()), })
        except ValueError:
            print("ERROR")
            # Handle the case where counter is not a valid integer
            counter = 0  # Set a default value or handle the error as appropriate
            return JsonResponse({'subtema': counter,
                                 'respostas': []})


def eliminarQuestionario(request, questID):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    questionario = get_object_or_404(Questionario, id=questID)
    questionario.delete()
    return redirect('questionarios:consultar-questionarios-admin')


def consultarPerguntas(request, questID):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    questionario = get_object_or_404(Questionario, id=questID)
    perguntas = PergQuest.objects.all().filter(questionarioid=questionario)
    for perg in perguntas:
        print(perg.perguntaid.pergunta, perg.perguntaid.tiporespostaid.type)
    print("chegou aqui")
    return render(request, 'questionario/consultar_questionarios_pergunta.html', {
        'questionario': questionario,
        'perguntas': perguntas,
        'perguntasSize': perguntas.count()
    })


def atividadeRoteirocsvEstatistica(request, questID=None):
    respostas = Resposta.objects.all()
    if not respostas.exists():
        return HttpResponse("Não existem respostas de questionário para o Dia Aberto do ano fornecido.", status=404)

    if questID is None:
        try:
            diaabertoid = Diaaberto.objects.filter(
                ano__lte=datetime.now().year).order_by('-ano').first().id
        except:
            return redirect('utilizadores:mensagem', 18)
    diaaberto = get_object_or_404(Diaaberto, id=questID)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    writer.writerow(['Perguntas utilizadas no questionário sobre almoços'])
    writer.writerow([])
    writer.writerow(['id', 'Pergunta', 'Tema', 'Tipo de Resposta'])
    for pergunta in Pergunta.objects.all().values_list('id', 'pergunta', 'temaid', 'tiporespostaid'):
        if pergunta[0] == 109 or pergunta[0] == 110 or pergunta[0] == 111 or pergunta[0] == 112:
            writer.writerow(pergunta)

    writer.writerow([])
    writer.writerow(['PerguntaID', 'Resposta', ])

    for resposta in Resposta.objects.all():
        if resposta.perguntaID_id in [109, 110, 111, 112]:
            writer.writerow([resposta.perguntaID_id, resposta.resposta])

    response['Content-Disposition'] = f'attachment;filename="Transportes_dia_aberto{diaaberto}.csv"'

    return response
