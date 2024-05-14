import django_tables2 as django_tables

from atividades.models import Tema
from configuracao.models import Diaaberto
from utilizadores.models import Administrador
from django.db.models import Count
from questionario.models import Questionario, TemaPerg, TipoResposta, EstadosQuest
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import F
import django_tables2 as django_tables
import django_tables2 as tables


class QuestionarioTable(django_tables.Table):
    titulo = django_tables.Column('titulo')
    # ano = django_tables.Column(accessor='getQuestionarioDateID')
    estado = django_tables.Column(accessor='getQuestionarioEstado', attrs={"th": {"width": "130"}})
    acoes = django_tables.Column('Ações', empty_values=(),
                                 orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        model = Questionario
        sequence = ('titulo', 'estado', 'acoes')

    def before_render(self, request):
        self.columns.hide('id')
        # self.columns.hide('dateid')
        self.columns.hide('estadoquestid')

    # def order_ano(self, queryset, is_descending):
    #     # Ordenar pelo campo associado (exemplo: `dateid`):
    #     queryset = queryset.order_by(F('dateid').desc() if is_descending else F('dateid').asc())
    #     return (queryset, True)

    def render_estado(self, record):
        if (record.getQuestionarioEstado == 'pendente'):
            estado = "Pendente"
            cor = "is-warning"
        elif (record.getQuestionarioEstado == 'validado'):
            estado = "Validado"
            cor = "is-success"
        elif (record.getQuestionarioEstado == 'arquivado'):
            estado = "Arquivado"
            cor = "is-secondary"
        elif (record.getQuestionarioEstado == 'publicado'):
            estado = "Publicado"
            cor = "is-info"
        elif (record.getQuestionarioEstado == 'concluido'):
            estado = "Concluido"
            cor = "is-primary"
        return format_html(f"""
                <span class="tag {cor}" style="font-size: small; min-width: 110px;">
                    {estado}
                </span>
                """)

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
        quarto_botao = """<span class="icon"></span>"""
        if record.getQuestionarioEstado == "concluido":
            primeiro_botao = f"""
                           <a data-tooltip="Arquivar" href="{reverse('questionarios:arquivar-questionario', args=[record.getQuestionarioID])}">
                               <span class="icon">
                                   <i class="fas fa-archive" aria-hidden="true" style="color: #F4B400"></i>
                               </span>
                           </a>
                           """
        if record.getQuestionarioEstado == "validado":
                quarto_botao = f"""
                               <a data-tooltip="Publicar" href="{reverse('questionarios:publicar-questionario', args=[record.getQuestionarioID])}">
                                   <span class="icon">
                                        <i class="fas fa-upload" style="color:#DB2323"></i>
                                   </span>
                               </a>
                           """

        segundo_botao = """<span class="icon"></span>"""

        terceiro_botao = """<span class="icon"></span>"""



        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
            {terceiro_botao}
            {quarto_botao}
            
        </div>
        """)


class TemaPergTable(django_tables.Table):
    perg_count = django_tables.Column('Perguntas com o Tema', accessor='get_num_perguntas')
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False)

    class Meta:
        model = TemaPerg

    def before_render(self, request):
        self.columns.hide('id')

    def order_perg_count(self, queryset, is_descending):
        # Anotar o queryset para contar as perguntas por tema
        queryset = queryset.annotate(perg_count=Count('pergunta'))

        # Ordenar pelo campo anotado, perg_count
        queryset = queryset.order_by(("-" if is_descending else "") + "perg_count")

        return queryset, True


class TipoRespostaTable(django_tables.Table):
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False)

    class Meta:
        model = TipoResposta

    def before_render(self, request):
        self.columns.hide('id')

    # def order_perguntas_count(self, queryset, is_descending):
    #     # print("entraste na ordem de perguntas")
    #     # print(queryset)
    #     queryset = queryset.annotate(perg_count=Count('pergunta')).order_by(("" if is_descending else "-") + "perg_count")
    #     return (queryset, True)


class DiaabertoTable(django_tables.Table):
    ano = django_tables.Column('Ano')
    questionarioid = django_tables.Column('Questionário', accessor='questionarioid.titulo')

    class Meta:
        model = Diaaberto
        fields = ('ano', 'questionarioid')  # Define as colunas a serem exibidas


class EstadoTable(tables.Table):
    cor = tables.Column('Cor', accessor='getEstadoCor', orderable=False)
    acoes = tables.Column('Ações', empty_values=(), orderable=False)
    id = tables.Column('Id', accessor='getEstadoId', orderable=False)

    class Meta:
        model = EstadosQuest
        sequence = ('nome', 'cor', 'acoes')

    def definir_javascript(self):
        return format_html('<script type="text/javascript" src="{}"></script>', '{% static "js/js_custom.js" %}')

    def before_render(self, request):
        self.columns.hide('id')

    def render_cor(self, record):
        return format_html(f"""
                     <span class="tag is-warning" style="background-color: {record.getEstadoCor}; font-size: small; min-width: 12vw;">
                    </span>
                    """)

    def render_acoes(self, record):
        primeiro_botao = f"""
                           <a data-tooltip="Editar" href="{reverse('questionarios:editarEstado', kwargs={'estados_id': record.getEstadoId})}">
                               <span class="icon">
                                   <i class="fas fa-edit" aria-hidden="true" style="color: #F4B400"></i>
                               </span>
                           </a>
                       """

        if Questionario.objects.filter(estadoquestid=record.getEstadoId).exists():
            segundo_botao = f"""
                                        <a data-tooltip="eliminar" onclick="alert2.render('O estado está a ser utilizado num questionário.<strong>Não o pode apagar.</strong>','{reverse('questionarios:consultar-estados-admin')}')">
                                            <span class="icon is-small">
                                                <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                                            </span>
                                        </a> 
                                    """
        else:
            segundo_botao = f"""
                            <a data-tooltip="Eliminar" onclick="alert.render('Tem a certeza que pretende eliminar este estado?','{reverse('questionarios:eliminarEstado', kwargs={'estados_id': record.getEstadoId})}')">
                                <span class="icon is-small">
                                    <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                                </span>
                            </a> 
                        """

        return format_html(f"""
                           {primeiro_botao}
                           {segundo_botao}
                   """)