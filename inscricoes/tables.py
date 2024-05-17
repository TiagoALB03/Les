import django_tables2 as tables
from .models import Inscricao, Escola
from configuracao.models import Diaaberto, Departamento, Unidadeorganica, Campus
from atividades.models import Atividade
import itertools
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Max, Min, OuterRef, Subquery
from inscricoes.models import Inscricaosessao


class InscricoesTable(tables.Table):
    grupo = tables.Column('Grupo', accessor='id', attrs={"th": {"width": "65"}})
    horario = tables.Column(verbose_name='Horário')
    nalunos = tables.Column(verbose_name='Qtd', attrs={
                            "abbr": {"title": "Quantidade"}, "th": {"width": "48"}})
    acoes = tables.Column('Ações', empty_values=(),
                          orderable=False, attrs={"th": {"width": "85"}})
    turma = tables.Column(empty_values=())

    class Meta:
        model = Inscricao
        sequence = ('grupo', 'dia', 'horario', 'escola', 'areacientifica',
                    'turma', 'nalunos', 'acoes')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('ano')
        self.columns.hide('areacientifica')
        self.columns.hide('participante')
        self.columns.hide('diaaberto')
        self.columns.hide('meio_transporte')
        self.columns.hide('hora_chegada')
        self.columns.hide('local_chegada')
        self.columns.hide('entrecampi')
        self.columns.hide('individual')

    def order_horario(self, queryset, is_descending):
        queryset = queryset.annotate(inicio=Subquery(
            Inscricaosessao.objects.filter(inscricao=OuterRef('pk'))
            .values('inscricao')
            .annotate(inicio=Min('sessao__horarioid__inicio'))
            .values('inicio')
        )).order_by(("-" if is_descending else "") + "inicio")
        return (queryset, True)

    def render_turma(self, value, record):
        if not record.ano:
            return format_html("(Individual)")
        return format_html(f"{record.ano}º {value}, {record.areacientifica}")

    def render_acoes(self, record):
        return format_html(f"""
        <div>
            <a href='{reverse("inscricoes:consultar-inscricao", kwargs={"pk": record.pk})}'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            <a onclick="alert.render('Tem a certeza que pretende eliminar esta inscrição?','{reverse("inscricoes:apagar-inscricao", kwargs={"pk": record.pk})}')"
                data-tooltip="Apagar">
                <span class="icon has-text-danger">
                    <i class="mdi mdi-trash-can mdi-24px"></i>
                </span>
            </a>
        </div>
        """)
