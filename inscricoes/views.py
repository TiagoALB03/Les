from django.shortcuts import get_object_or_404, redirect, render
from inscricoes.models import Inscricao, Inscricaosessao, Responsavel
from inscricoes.utils import add_vagas_sessao, enviar_mail_confirmacao_inscricao, init_form, nao_tem_permissoes, render_pdf, save_form, update_context, update_post
from atividades.models import Atividade, Sessao
from atividades.serializers import AtividadeSerializer
from atividades.filters import AtividadeFilter
from inscricoes.forms import AlmocoForm, InfoForm, InscricaoForm, ResponsavelForm, SessoesForm, TransporteForm
from utilizadores.models import Administrador, Coordenador, Participante
from utilizadores.views import user_check
from django.http import HttpResponseRedirect
from django.urls import reverse
from inscricoes.tables import InscricoesTable
from inscricoes.filters import InscricaoFilter
from django.db.models import Exists, OuterRef
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from formtools.wizard.views import SessionWizardView
from django.views import View
from django_tables2 import SingleTableMixin
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.views import FilterView
from configuracao.models import Departamento, Diaaberto
from datetime import datetime
import pytz
from configuracao.tests.test_models import create_open_day
from _datetime import timedelta


def InscricaoPDF(request, pk):
    """ View que gera um PDF com os detalhes da inscrição """
    inscricao = get_object_or_404(Inscricao, pk=pk)
    erro_permissoes = nao_tem_permissoes(request, inscricao)
    if erro_permissoes and not request.user.groups.filter(name="Colaborador").exists():
        return erro_permissoes
    ano = inscricao.diaaberto.ano
    context = {
        'request': request,
        'inscricao': inscricao,
        'ano': ano,
    }
    return render_pdf("inscricoes/pdf.html", context, f"dia_aberto_ualg_{ano}.pdf")


class AtividadesAPI(ListAPIView):
    """ View que gera uma API readonly com as informações das Atividades e das suas sessões
        que vai ser usada para fazer inscrições nas sessões """
    class AtividadesPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = 'nome'
    filter_backends = (SearchFilter,
                       OrderingFilter, DjangoFilterBackend)
    queryset = Atividade.objects.filter(estado="Aceite")
    serializer_class = AtividadeSerializer
    pagination_class = AtividadesPagination
    filterset_class = AtividadeFilter


class CriarInscricao(SessionWizardView):
    """ View que gera o formulário com passos para criar uma nova inscrição """
    form_list = [
        ('info', InfoForm),
        ('responsaveis', ResponsavelForm),
        ('escola', InscricaoForm),
        ('transporte', TransporteForm),
        ('almoco', AlmocoForm),
        ('sessoes', SessoesForm),
    ]

    def dispatch(self, request, *args, **kwargs):
        _user_check = user_check(request, [Participante])
        if _user_check['exists']:
            participante = _user_check['firstProfile']
            diaaberto = Diaaberto.current()
            if diaaberto is None:
                return redirect('utilizadores:mensagem', 12)
            if datetime.now(pytz.UTC) < diaaberto.datainscricaoatividadesinicio or datetime.now(pytz.UTC) > diaaberto.datainscricaoatividadesfim:
                m = f"Período de abertura das inscrições: {diaaberto.datainscricaoatividadesinicio.strftime('%d/%m/%Y')} até {diaaberto.datainscricaoatividadesfim.strftime('%d/%m/%Y')}"
                return render(request=request,
                              template_name="mensagem.html", context={'m': m, 'tipo': 'error', 'continuar': 'on'})
            self.instance_dict = {
                'responsaveis': Responsavel(nome=f"{participante.first_name} {participante.last_name}", email=participante.email, tel=participante.contacto)
            }
        else:
            return _user_check['render']
        return super(CriarInscricao, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        update_context(context, self.steps.current, self)
        if self.steps.current != 'info':
            context.update({
                'individual': self.get_cleaned_data_for_step('info')['individual']
            })
        visited = []
        for step in self.form_list:
            cleaned_data = self.get_cleaned_data_for_step(step)
            if cleaned_data:
                visited.append(True)
            else:
                visited.append(False)
        context.update({
            'visited': visited
        })
        return context

    def get_template_names(self):
        return [f'inscricoes/inscricao_wizard_{self.steps.current}.html']

    def post(self, request, *args, **kwargs):
        # Envia a informação extra necessária para o formulário atual, após preenchê-lo.
        # Necessário para algumas validações especiais de backend, como verificar o número de alunos
        # inscritos para verificar inscritos nos almoços e nas sessões.
        current_step = request.POST.get(
            'criar_inscricao-current_step', self.steps.current)
        update_post(current_step, request.POST, self)
        go_to_step = self.request.POST.get(
            'wizard_goto_step', None)  # get the step name
        if go_to_step is not None:
            form = self.get_form(data=self.request.POST,
                                 files=self.request.FILES)

            if self.get_cleaned_data_for_step(current_step):
                if form.is_valid():
                    self.storage.set_step_data(self.steps.current,
                                               self.process_step(form))
                    self.storage.set_step_files(self.steps.current,
                                                self.process_step_files(form))
                else:
                    return self.render(form)
        return super(CriarInscricao, self).post(*args, **kwargs)

    def done(self, form_list, form_dict, **kwargs):
        # Guardar na Base de Dados
        responsaveis = form_dict['responsaveis'].save(commit=False)
        almoco = form_dict['almoco'].save(commit=False)
        inscricao = form_dict['escola'].save(commit=False)
        inscricao.participante = Participante.objects.filter(
            utilizador_ptr_id=self.request.user.id).first()
        inscricao.meio_transporte = form_dict['transporte'].cleaned_data['meio']
        if(form_dict['transporte'].cleaned_data['meio'] != 'outro'):
            inscricao.hora_chegada = form_dict['transporte'].cleaned_data['hora_chegada']
            inscricao.local_chegada = form_dict['transporte'].cleaned_data['local_chegada']
        inscricao.entrecampi = form_dict['transporte'].cleaned_data['entrecampi']
        inscricao.save()
        sessoes = form_dict['sessoes'].cleaned_data['sessoes']
        for sessaoid in sessoes:
            if sessoes[sessaoid] > 0:
                inscricao_sessao = Inscricaosessao(sessao=Sessao.objects.get(
                    pk=sessaoid), nparticipantes=sessoes[sessaoid], inscricao=inscricao)
                add_vagas_sessao(sessaoid, -sessoes[sessaoid])
                inscricao_sessao.save()
        responsaveis.inscricao = inscricao
        responsaveis.save()
        if almoco is not None:
            almoco.inscricao = inscricao
            almoco.save()
        enviar_mail_confirmacao_inscricao(self.request, inscricao.pk)
        return render(self.request, 'inscricoes/consultar_inscricao_submissao.html', {
            'inscricao': inscricao,
        })


class ConsultarInscricao(View):
    """ View que gera o formulário com passos para consultar ou alterar uma inscrição """
    template_prefix = 'inscricoes/consultar_inscricao'
    step_names = [
        'responsaveis',
        'escola',
        'transporte',
        'almoco',
        'sessoes',
        'submissao'
    ]

    def get(self, request, pk, step=0, alterar=False):
        inscricao = get_object_or_404(Inscricao, pk=pk)
        erro_permissoes = nao_tem_permissoes(request, inscricao)
        if erro_permissoes:
            return erro_permissoes
        if user_check(request, [Participante])['exists'] and datetime.now(pytz.UTC) > inscricao.diaaberto.datainscricaoatividadesfim:
            m = f"Não pode alterar a inscrição fora do período: {inscricao.diaaberto.datainscricaoatividadesinicio.strftime('%d/%m/%Y')} até {inscricao.diaaberto.datainscricaoatividadesfim.strftime('%d/%m/%Y')}"
            return render(request=request, template_name="mensagem.html", context={'m': m, 'tipo': 'error', 'continuar': 'on'})
        form = init_form(self.step_names[step], inscricao)
        context = {'alterar': alterar,
                   'pk': pk,
                   'step': step,
                   'individual': inscricao.individual,
                   'form': form,
                   }
        update_context(context, self.step_names[step], inscricao=inscricao)
        return render(request, f"{self.template_prefix}_{self.step_names[step]}.html", context)

    def post(self, request, pk, step=0, alterar=False):
        inscricao = get_object_or_404(Inscricao, pk=pk)
        erro_permissoes = nao_tem_permissoes(request, inscricao)
        if erro_permissoes:
            return erro_permissoes
        context = {}
        if alterar:
            if request.user.groups.filter(name="Participante").exists() and datetime.now(pytz.UTC) > inscricao.diaaberto.datainscricaoatividadesfim:
                m = f"Não pode alterar a inscrição fora do período: {inscricao.diaaberto.datainscricaoatividadesinicio.strftime('%d/%m/%Y')} até {inscricao.diaaberto.datainscricaoatividadesfim.strftime('%d/%m/%Y')}"
                return render(request=request, template_name="mensagem.html", context={'m': m, 'tipo': 'error', 'continuar': 'on'})
            update_post(self.step_names[step],
                        request.POST, inscricao=inscricao)
            form = init_form(self.step_names[step], inscricao, request.POST)
            inscricoessessao = inscricao.inscricaosessao_set.all()
            if self.step_names[step] == 'sessoes':
                for inscricao_sessao in inscricoessessao:
                    add_vagas_sessao(inscricao_sessao.sessao.id,
                                     inscricao_sessao.nparticipantes)
            if form.is_valid():
                save_form(request, self.step_names[step], form, inscricao)
                return HttpResponseRedirect(reverse('inscricoes:consultar-inscricao', kwargs={'pk': pk, 'step': step}))
            if self.step_names[step] == 'sessoes':
                for inscricao_sessao in inscricoessessao:
                    add_vagas_sessao(inscricao_sessao.sessao.id,
                                     -inscricao_sessao.nparticipantes)
        context.update({'alterar': alterar,
                        'pk': pk,
                        'step': step,
                        'individual': inscricao.individual,
                        'form': form,
                        })
        update_context(context, self.step_names[step], inscricao=inscricao)
        return render(request, f"{self.template_prefix}_{self.step_names[step]}.html", context)


class ConsultarInscricoes(SingleTableMixin, FilterView):
    """ View base para gerar tabelas com inscrições """
    table_class = InscricoesTable

    filterset_class = InscricaoFilter

    table_pagination = {
        'per_page': 10
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super(ConsultarInscricoes, self).get_filterset_kwargs(
            filterset_class)
        if kwargs["data"] is None:
            kwargs["data"] = {"diaaberto": Diaaberto.objects.filter(
                ano__lte=datetime.now().year).order_by('-ano').first().id}
        elif "diaaberto" not in kwargs["data"]:
            kwargs["data"] = kwargs["data"].copy()
            kwargs["data"]["diaaberto"] = Diaaberto.objects.filter(
                ano__lte=datetime.now().year).order_by('-ano').first().id
        return kwargs


class MinhasInscricoes(ConsultarInscricoes):
    """ View que gera uma tabela com as inscrições do participante """
    template_name = 'inscricoes/consultar_inscricoes_participante.html'

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Participante])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Inscricao.objects.filter(participante__user_ptr=self.request.user)


class InscricoesUO(ConsultarInscricoes):
    """ View que gera uma tabela com as inscrições com pelo menos uma sessão do departamento
    do coordenador """
    template_name = 'inscricoes/consultar_inscricoes_coordenador.html'

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[
            Coordenador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        coordenador = Coordenador.objects.get(user_ptr=request.user)
        self.queryset = Inscricao.objects.filter(
            Exists(Inscricaosessao.objects.filter(
                inscricao=OuterRef('pk'),
                sessao__atividadeid__professoruniversitarioutilizadorid__faculdade=coordenador.faculdade
            ))
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coordenador = Coordenador.objects.get(user_ptr=self.request.user)
        context["departamentos"] = list(
            map(lambda x: (x.id, x.nome), Departamento.objects.filter(unidadeorganicaid=coordenador.faculdade)))
        return context


class InscricoesAdmin(ConsultarInscricoes):
    """ View que gera uma tabela com as todas as inscrições """
    template_name = 'inscricoes/consultar_inscricoes_admin.html'

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[
            Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departamentos"] = list(
            map(lambda x: (x.id, x.nome), Departamento.objects.all()))
        return context


def ApagarInscricao(request, pk):
    """ View que apaga uma inscrição """
    inscricao = get_object_or_404(Inscricao, pk=pk)
    erro_permissoes = nao_tem_permissoes(request, inscricao)
    if erro_permissoes:
        return erro_permissoes
    inscricaosessao_set = inscricao.inscricaosessao_set.all()
    for inscricaosessao in inscricaosessao_set:
        sessaoid = inscricaosessao.sessao.id
        nparticipantes = inscricaosessao.nparticipantes
        add_vagas_sessao(sessaoid, nparticipantes)
    inscricao.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def estatisticas(request, diaabertoid=None):
    """ View que mostra as estatísticas do Dia Aberto """
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    if diaabertoid is None:
        try:
            diaabertoid = Diaaberto.objects.filter(
                ano__lte=datetime.now().year).order_by('-ano').first().id
        except:
            return redirect('utilizadores:mensagem', 18)
    diaaberto = get_object_or_404(Diaaberto, id=diaabertoid)
    numdays = int((diaaberto.datadiaabertofim -
                   diaaberto.datadiaabertoinicio).days)+1
    dias = [(diaaberto.datadiaabertoinicio + timedelta(days=x)
             ).strftime("%d/%m/%Y") for x in range(numdays)]
    return render(request, 'inscricoes/estatisticas.html', {
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
        'meios': Inscricao.MEIO_TRANSPORTE_CHOICES,
    })
