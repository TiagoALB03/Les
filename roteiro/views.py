from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from atividades.models import Atividade, Sessao
from roteiro.filters import RoteirosFilter
from roteiro.models import Roteiro
from roteiro.tables import RoteiroTable
from utilizadores.models import Administrador, Coordenador
from utilizadores.views import user_check


# Create your views here.

class roteiroCoordenador(SingleTableMixin, FilterView):
    table_class = RoteiroTable
    template_name = 'roteiros/roteirosCoordenador.html'
    table_pagination = {
        'per_page': 5
    }
    filterset_class = RoteirosFilter

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Coordenador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table

        # Adicionando dados do roteiro ao contexto
        roteiros = Roteiro.objects.all()  # Recupera todos os roteiros (você pode ajustar a consulta conforme necessário)
        context['roteiros'] = roteiros

        return context


def consultarRoteiro(request,roteiro_id):
    user_check_var = user_check(request=request, user_profile=[Coordenador])
    if user_check_var.get('exists') == False:
        return user_check_var.get('render')
    if roteiro_id is not None:
        roteiro = Roteiro.objects.get(id=roteiro_id)
        allowMore, allowDelete = False, False

    return render(request=request,
                  template_name='roteiros/consultar_roteiros_tabela.html',context={
                    'roteiros': Roteiro.objects.get(id=roteiro_id),
                    'sessoes': Sessao.objects.all().filter(roteiro=roteiro_id),
                    'atividades': Atividade.objects.all().filter(roteiro=roteiro_id),
                  })