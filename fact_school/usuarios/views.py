from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  AvaliacaoFACT, RespostaFACT, Turma, Equipe, Criterion
from .forms import  CriarAvaliacaoFACTForm, CriarEquipeForm, ResponderAvaliacaoFACTForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.timezone import now

User = get_user_model()

def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():   
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                if user.is_superuser:
                    return redirect('/admin/')
                elif user.groups.filter(name='Professores').exists():
                    return redirect('professor_home')
                elif user.groups.filter(name='Alunos').exists():
                    return redirect('aluno_home')
                else:
                    return redirect('')
                
        else:
            return render(request, 'usuarios/login.html', {'form': form,'error': 'Usuário ou senha inválidos'})
        
    return render(request, 'usuarios/login.html', {'form': form})

def is_professor(user):
    return user.groups.filter(name='Professores').exists()

# Decorador para restringir acesso
professor_required = user_passes_test(is_professor)

def is_aluno(user):
    return user.groups.filter(name='Alunos').exists()

aluno_required = user_passes_test(is_aluno)



@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect('login')
    
@login_required
@aluno_required
def aluno_home(request):
    '''avaliacoes_disponiveis=AvaliacaoFACT.objects.filter(
        turma__alunos=request.user,
        inicio__lte=now(),
        fim__gte=now()
    ).distinct()'''
    avaliacoes_disponiveis = AvaliacaoFACT.objects.filter(
        avaliado__in=request.user.equipes.values_list('integrantes', flat=True)
    ).distinct()
    equipes = Equipe.objects.filter(integrantes=request.user)
    return render(request, 'usuarios/aluno_home.html', {'avaliacoes' : avaliacoes_disponiveis, 'equipes':equipes},)
    
@login_required
@professor_required
def professor_home(request):
    return render(request, 'usuarios/professor_home.html')
'''
@login_required
@aluno_required
def responder_fact(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    avaliados = equipe.integrantes.exclude(id=request.user.id)
    criterios = Criterion.objects.all()
    if request.method == "POST":
        form = CriarAvaliacaoFACTForm(request.POST, avaliados=avaliados)
        if form.is_valid():
            for avaliado in avaliados:
                justificativa = form.cleaned_dataf('justificativa_{avaliado.id}')
                for criterio in criterios:
                    nota = form.cleaned_data(f'nota_{avaliado.id}_{criterio.id}')
                    AvaliacaoFACT.objects.create(
                        avaliador=request.user,
                        avaliado=avaliado,
                        criterio=criterio,
                        nota=nota,
                        justificativa=justificativa,
                    )
            return redirect('aluno_home')
    else:
        form = CriarAvaliacaoFACTForm(avaliados=avaliados)
    return render(request, 'usuarios/responder_fact.html', {'form': form, 'equipe': equipe})
'''
#responder_fact TESTE
def responder_fact(request, equipe_id):
    criterios = Criterion.objects.all()  # Busca todos os critérios
    equipe = get_object_or_404(Equipe, id=equipe_id)
    integrantes = equipe.integrantes.exclude(id=request.user.id)
    if request.method == "POST":
        for integrante in integrantes:
            for criterio in criterios:
                nota = request.POST.get(f'nota_{integrante.id}_{criterio.id}')
                justificativa = request.POST.get(f'justificativa_{integrante.id}')
                
                if nota:
                    AvaliacaoFACT.objects.create(
                        avaliador=request.user,
                        avaliado=integrante,
                        criterio=criterio,
                        nota=nota,
                        justificativa=justificativa,
                    )
        return redirect('aluno_home')
    
    return render(request, 'usuarios/responder_fact.html', {'equipe': integrantes, 'criterios': criterios})

@login_required
@professor_required
def configurar_avaliacao_fact(request):
    if request.method == "POST":
        form = CriarAvaliacaoFACTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('professor_home')
    else:
        form = CriarAvaliacaoFACTForm()
    return render(request, 'usuarios/aluno/p1FACT.html', {'form': form})
@login_required
@professor_required
def criar_equipe(request):
    if request.method == 'POST':
        form = CriarEquipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('professor_home')
    else:
        form = CriarEquipeForm()
        form.fields['turma'].queryset = Turma.objects.all()  # Ensure queryset is not None
    return render(request, 'usuarios/criar_equipe.html', {'form': form})

@login_required
@aluno_required
def responder_avaliacao_fact(request, avaliacao_id):
    avaliacao = get_object_or_404(AvaliacaoFACT, id=avaliacao_id)
    if not avaliacao.esta_disponivel():
        return redirect('aluno_home')
    
    criterios = ["Pensamento Crítico", "Comunicação", "Colaboração", "Qualidade", "Presença"]
    if request.method == "POST":
        form = ResponderAvaliacaoFACTForm(request.POST, criterios=criterios)
        if form.is_valid():
            for criterio in criterios:
                RespostaFACT.objects.create(
                    avaliacao=avaliacao,
                    avaliador=request.user,
                    avaliado=request.user, #Placeholder para quando integrar com equipes
                    criterio=criterio,
                    nota=form.cleaned_data[f'criterio_{criterio}'],
                    justificativa=form.cleaned_data[f'justificativa_{criterio}'],
                )
            return redirect('aluno_home')
    else:
        form = ResponderAvaliacaoFACTForm(criterios=criterios)
    return render(request, 'usuarios/aluno/p2FACT.html', {'form': form, 'avaliacao': avaliacao})
    
@login_required
@professor_required
def visualizar_resultados_fact(request, avaliacao_id):
    avaliacao = get_object_or_404(AvaliacaoFACT, id=avaliacao_id)
    respostas = avaliacao.respostas.all()
    medias = {}
    for resposta in respostas:
        if resposta.avaliado not in medias:
            medias[resposta.avaliado] = []
        medias[resposta.avaliado].append(resposta.nota)
    for avaliado in medias:
        medias[avaliado] = sum(medias[avaliado]) / len(medias[avaliado])
    return render(request, 'resultadosFACT.html', {'avaliacao': avaliacao, 'medias': medias, 'respostas': respostas})

def listar_turmas(request):
    turmas = Turma.objects.filter(professor=request.user)