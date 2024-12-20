from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  AvaliacaoFACT, Turma, Equipe, Criterion, RelatorioAvaliacao, DisponibilidadeAvaliacao
from .forms import CriarEquipeForm, DisponibilizarAvaliacaoForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
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
    turmas = request.user.turmas_inscritas.all()
    equipes = Equipe.objects.filter(integrantes=request.user)
    now_time = now()
    disponibilidades = DisponibilidadeAvaliacao.objects.filter(turma__in=turmas, inicio__lte=now_time, fim__gte=now_time)

    return render(request, 'usuarios/aluno_home.html', {
        'equipes': equipes,
        'turmas': turmas, 
        'disponibilidades': disponibilidades,
    })

@login_required
def verFACT(request):
    return render(request, 'usuarios/verFACT.html')

@login_required
@aluno_required
def equipe(request):
    equipes = Equipe.objects.filter(integrantes=request.user)
    return render(request, 'usuarios/equipe.html', {'equipes': equipes})
    
@login_required
@professor_required
def professor_home(request):
    turmas = Turma.objects.filter(professor=request.user)
    return render(request, 'usuarios/professor_home.html', {'turmas': turmas})


#responder_fact TESTE
def responder_fact(request, equipe_id):
    criterios = Criterion.objects.all() 
    equipe = get_object_or_404(Equipe, id=equipe_id)
    integrantes = equipe.integrantes.exclude(id=request.user.id)
    if request.method == "POST":
        for integrante in integrantes:
            justificativa = request.POST.get(f'justificativa_{integrante.id}')
            fact ={}
            for criterio in criterios:
                nota = request.POST.get(f'nota_{integrante.id}_{criterio.id}')
                fact[criterio] = nota
            if fact:
                for criterio, nota in fact.items():    
                    AvaliacaoFACT.objects.create(
                        avaliador=request.user,
                        avaliado=integrante,
                        criterio=criterio,
                        nota=nota,
                        justificativa=justificativa,
                    )
        
        for integrante in integrantes:
            relatorio = RelatorioAvaliacao(
                avaliador=request.user,
                avaliado=integrante,
            )
            relatorio.gerar_relatorio()

        return redirect('aluno_home')
    
    return render(request, 'usuarios/responder_fact.html', {'equipe': integrantes, 'criterios': criterios})


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
        form.fields['turma'].queryset = Turma.objects.all()  
    return render(request, 'usuarios/criar_equipe.html', {'form': form})

@professor_required
@login_required
def make_available(request):
    if request.method == "POST":
        form = DisponibilizarAvaliacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('professor_home')  
    else:
        form = DisponibilizarAvaliacaoForm()
    return render(request, 'usuarios/evalProf.html', {'form': form})


@login_required
@professor_required
def visualizar_avaliacoes(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    equipes = turma.equipes.all()
    alunos_da_turma = turma.alunos.all()

    alunos_avaliacoes = []
    for aluno in alunos_da_turma:
        relatorios = RelatorioAvaliacao.objects.filter(avaliado=aluno)
        criterios_e_notas = []
        justificativas = {}
        total_notas = 0
        total_avaliadores = 0

        for relatorio in relatorios:
            criterios_e_notas.extend(relatorio.criterios_e_notas)
            justificativas.update(relatorio.justificativas)
            
            nota_total_avaliador = sum(item['nota'] for item in relatorio.criterios_e_notas)
            total_notas += nota_total_avaliador
            total_avaliadores += 1
            
        media = (total_notas / total_avaliadores if total_avaliadores > 0 else None)/10
        alunos_avaliacoes.append({
            'aluno': aluno,
            'criterios_e_notas': criterios_e_notas,
            'justificativas': justificativas,
            'media': media,
            'relatorios': relatorios
        })

    return render(request, 'usuarios/visualizar_avaliacoes.html', {
        'turma': turma,
        'equipes': equipes,
        'alunos_avaliacoes': alunos_avaliacoes,
    })

@login_required
@professor_required
def listar_e_excluir_equipes(request):
    equipes = Equipe.objects.all()

    if request.method == 'POST':
        equipe_id = request.POST.get('equipe_id')
        equipe = get_object_or_404(Equipe, id=equipe_id)
        equipe.delete()
        return redirect('listar_e_excluir_equipes')

    return render(request, 'usuarios/listar_e_excluir_equipes.html', {'equipes': equipes})
