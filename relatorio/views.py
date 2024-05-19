from datetime import timedelta, datetime

from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404, redirect

from atividades.models import Atividade
from configuracao.models import Transporte, Campus, Diaaberto, Transportehorario, Departamento
from inscricoes.models import Inscricaotransporte
from inscricoes.utils import render_pdf
from utilizadores.models import Administrador
from utilizadores.views import user_check


from atividades.filters import *



def relatorio_Transporte(request, diaabertoid=None):
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
    return render(request, 'relatorio/escolherAnoRelatorioTransporte.html', {
        'diaaberto': diaaberto,
        'diasabertos': Diaaberto.objects.all(),
        'ultimo_dia_aberto': Diaaberto.objects.order_by('-datadiaabertofim').first(),
    })
def InscricaoPDF(request, diaabertoid):
    filterset_class = Transportehorario.objects.filter(transporte__diaaberto=diaabertoid)
    info_with_attributes = []
    for item in filterset_class:
        print("dados", item)
    for item in filterset_class:
        espacoAtual = item.get_capacidade
        espacoOcupado = 0
        for object in Inscricaotransporte.objects.filter(transporte=item.id):
            espacoOcupado += object.npassageiros
        espacoAtual -= int(espacoOcupado)
        info_with_attributes.append({
            'obj': item,
            'ocupado': espacoOcupado,
            'disponivel': espacoAtual
        })
    ano = Diaaberto.objects.get(id=diaabertoid).ano
    filename = f"relatorioTransporte{ano}.pdf"
    checkRespostasAmmount = len(info_with_attributes)
    context = {'info': info_with_attributes, 'checkRespostasAmmount': checkRespostasAmmount, 'ano':ano}
    return render_pdf("relatorio/pdfTransporte.html", context, filename)




def relatorio_Atividades(request, diaabertoid=None):
    """ View que mostra as estatísticas das Atividades """
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
    return render(request, 'relatorio/escolherAnoRelatorioAtividades.html', {
        'diaaberto': diaaberto,
        'diasabertos': Diaaberto.objects.all(),
        'ultimo_dia_aberto': Diaaberto.objects.order_by('-datadiaabertofim').first(),
    })

def AtividadesPDF(request, diaabertoid):
    atividades = Atividade.objects.filter(diaabertoid=diaabertoid)
    info_with_attributes = []
    for atividade in atividades:
        sessoes = Sessao.objects.filter(atividadeid=atividade.id)
        for sessao in sessoes:
            info_with_attributes.append({
                'atividade': atividade,
                'sessao': sessao
            })
    ano = Diaaberto.objects.get(id=diaabertoid).ano
    filename = f"relatorioAtividades{ano}.pdf"
    checkRespostasAmmount = len(info_with_attributes)
    context = {'info': info_with_attributes, 'checkRespostasAmmount': checkRespostasAmmount, 'ano':ano}
    return render_pdf("relatorio/pdfAtividades.html", context, filename)


