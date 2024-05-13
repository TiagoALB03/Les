from django.forms import *

from atividades.models import Tema
from questionario.models import Questionario, Pergunta, TemaPerg, TipoResposta, PergQuest


# from questionario.models import Questionario, Pergunta, Resposta

class QuestionarioForm(ModelForm):
    class Meta:
        model = Questionario
        exclude = ['id', 'estadoquestid']
        widgets = {
            'titulo': TextInput(attrs={'class': 'input'}),
        }

class Questionario2Form(ModelForm):
    class Meta:
        model = Questionario
        exclude = ['id', 'estadoquestid', 'titulo']
        widgets = {}


class PerguntasForm(ModelForm):
    class Meta:
        model = Pergunta
        exclude = ['id', 'questionarioid', 'subtemaid']
        widgets = {
            'pergunta': TextInput(attrs={'class': 'input'}),
        }


class TemaFormPerg(ModelForm):
    class Meta:
        model = TemaPerg
        exclude = ['id']
        widgets = {
            'tema': TextInput(attrs={'class': 'input'}),
        }

class TipoRespostaForm(ModelForm):
    class Meta:
        model = TipoResposta
        exclude = ['id']
        widgets = {
            'tiporesposta' : TextInput(attrs={'class': 'input'}),
        }


class PergQuestForm(ModelForm):
    class Meta:
        model = PergQuest
        exclude = ['id']
        widgets = {}
