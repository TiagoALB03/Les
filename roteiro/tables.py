import django_tables2 as django_tables
import django_tables2 as tables

from roteiro.models import Roteiro
from utilizadores.models import Administrador
from questionario.models import Questionario, EstadosQuest
from django.utils.html import format_html
from django.urls import reverse


class RoteiroTable(django_tables.Table):
    nome = django_tables.Column('Nome', accessor='getRoteiroNome', orderable=False)
    ano = django_tables.Column('Ano', accessor='getRoteiroDiaAbertoID', orderable=False)
    coordenador = django_tables.Column('Coordenador', accessor='getRoteiroCoordenadorID', orderable=False)
    acoes = django_tables.Column('Ações', empty_values=(), orderable=False)

    class Meta:
        model = Roteiro
        sequence = ('nome', 'coordenador', 'ano', 'acoes')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('diaabertoid')
        self.columns.hide('coordenadorID')
        self.columns.hide('participantesmaximo')
        self.columns.hide('duracaoesperada')
        self.columns.hide('publicoalvo')

    def render_estado(self, record):
        return format_html(f"""
                 <span class="tag is-warning" style="background-color: {record.getRoteiroCor}; font-size: small; min-width: 110px;">
                    {record.getRoteiroEstado}
                </span>
                """)

    def render_acoes(self, record):
        if record.estado.nome != "Aceite" or record.diaabertoid.ano == 2024:
            segundo_botao = f"""
                       """
        else:
            segundo_botao = f"""
                                    <a href='{reverse("roteiros:duplicar-roteiro", args={record.pk})}'
                                        data-tooltip="Duplicar">
                                        <span class="mdi mdi-content-copy">

                                        </span>
                                    </a>
                                    """
        primeiro_botao = f"""
                           <a data-tooltip="Consultar detalhes" href="{reverse('roteiros:consultarRoteiro', kwargs={'roteiro_id': record.getRoteiroID})}">
                               <span class="icon">
                                   <i class="fas fa-eye" aria-hidden="true" style="color: #3A99E2"></i>
                               </span>
                           </a>
                       """
        return format_html(f"""
                           {primeiro_botao}
                           {segundo_botao}
                   """)
