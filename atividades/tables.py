import django_tables2 as tables
from atividades.models import *
from django.utils.html import format_html
from django.db.models import Count

class CoordAtividadesTable(tables.Table):
    
    #acoes = tables.Column('Operações', empty_values=())
    professoruniversitarioutilizadorid = tables.Column('Professor')
    datasubmissao = tables.Column('Data de Submissão')
    class Meta:
        model = Atividade
        sequence = ('nome','professoruniversitarioutilizadorid','tipo','datasubmissao','estado')
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('nrcolaboradoresnecessario')
        self.columns.hide('publicoalvo')
        #self.columns.hide('tipo')
        self.columns.hide('dataalteracao')
        self.columns.hide('duracaoesperada')
        self.columns.hide('participantesmaximo')
        self.columns.hide('espacoid')
        self.columns.hide('tema')
        self.columns.hide('diaabertoid')

    def render_estado(self,record):
        fancy_box = ""
        if record.estado == 'Aceite':
            fancy_box = f"""
            <span class="tag text is-success" style="width: 7rem;font-size: small;">Aceite</span>
            """
        elif record.estado == 'Pendente':
            fancy_box = f"""
            <span class="tag text is-warning" style="width: 7rem;font-size: small;">Pendente</span>
            """
        else:
            fancy_box = f"""
            <span class="tag text is-danger" style="width: 7rem;font-size: small;">Recusada</span>
            """          
        return format_html(fancy_box)


    def render_professoruniversitarioutilizadorid(self,record):
        return str(record.professoruniversitarioutilizadorid.full_name)


class ProfAtividadesTable(tables.Table):
    
    acoes = tables.Column('Operações', empty_values=())
    datasubmissao = tables.Column('Data de Submissão')
    coordenador = tables.Column('Coordenador Responsavel', empty_values=())
    class Meta:
        model = Atividade
        sequence = ('nome','tipo','datasubmissao','coordenador','estado', 'acoes')
        
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('nrcolaboradoresnecessario')
        self.columns.hide('publicoalvo')
        self.columns.hide('professoruniversitarioutilizadorid')
        self.columns.hide('dataalteracao')
        self.columns.hide('duracaoesperada')
        self.columns.hide('participantesmaximo')
        self.columns.hide('espacoid')
        self.columns.hide('tema')
        self.columns.hide('diaabertoid')

    def render_estado(self,record):
        fancy_box = ""
        if record.estado == 'Aceite':
            fancy_box = f"""
            <span class="tag text is-success" style="width: 7rem;font-size: small;">Aceite</span>
            """
        elif record.estado == 'Pendente':
            fancy_box = f"""
            <span class="tag text is-warning" style="width: 7rem;font-size: small;">Pendente</span>
            """
        else:
            fancy_box = f"""
            <span class="tag text is-danger" style="width: 7rem;font-size: small;">Recusada</span>
            """          
        return format_html(fancy_box)


    def render_coordenador(self,record):
        if record.get_coord() is not None:
            return format_html(record.get_coord().full_name)



    def render_acoes(self,record):
        sessoes= Sessao.objects.filter(atividadeid=record)
        for sessao in sessoes:
            if sessao.vagas != record.participantesmaximo:
                return format_html(f"""
                <div></div>
                 """)
        return format_html(f"""
            <div>
                    <a id='edit' href="{reverse('atividades:alterarAtividade', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                &nbsp;               
                    <a onclick="alert.render('Tem a certeza que pretende eliminar esta Atividade?','{reverse('atividades:eliminarAtividade', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
            </div> 
        """)



class AdminAtividadesTable(tables.Table):
    
    professoruniversitarioutilizadorid = tables.Column('Professor')
    datasubmissao = tables.Column('Data de Submissão')
    class Meta:
        model = Atividade
        sequence = ('nome','professoruniversitarioutilizadorid','tipo','datasubmissao','estado')
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('nrcolaboradoresnecessario')
        self.columns.hide('publicoalvo')
        self.columns.hide('dataalteracao')
        self.columns.hide('duracaoesperada')
        self.columns.hide('participantesmaximo')
        self.columns.hide('espacoid')
        self.columns.hide('tema')
        self.columns.hide('diaabertoid')

    def render_estado(self,record):
        fancy_box = ""
        if record.estado == 'Aceite':
            fancy_box = f"""
            <span class="tag text is-success" style="width: 7rem;font-size: small;">Aceite</span>
            """
        elif record.estado == 'Pendente':
            fancy_box = f"""
            <span class="tag text is-warning" style="width: 7rem;font-size: small;">Pendente</span>
            """
        else:
            fancy_box = f"""
            <span class="tag text is-danger" style="width: 7rem;font-size: small;">Recusada</span>
            """          
        return format_html(fancy_box)


    def render_professoruniversitarioutilizadorid(self,record):
        return str(record.professoruniversitarioutilizadorid.full_name)