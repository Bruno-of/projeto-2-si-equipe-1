from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  AvaliacaoFACT, RespostaFACT, Turma, Equipe  # Ensure you have imported the necessary models
from .forms import  CriarAvaliacaoFACTForm, ResponderAvaliacaoFACTForm, CriarEquipeForm
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
    avaliacoes_disponiveis=AvaliacaoFACT.objects.filter(
        turma__alunos=request.user,
        inicio__lte=now(),
        fim__gte=now()
    ).distinct()
    return render(request, 'usuarios/aluno_home.html', {'avaliacoes' : avaliacoes_disponiveis},)
    
@login_required
@professor_required
def professor_home(request):
    return render(request, 'usuarios/professor_home.html')

'''
@professor_required
@login_required
def make_available(request):
    if request.method == "POST":
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user  # Atribuir o avaliador automaticamente
            evaluation.save()
            form.save_m2m()
            messages.success(request, 'Avaliação criada com sucesso!')
            return redirect('evalProf')  # Redireciona para a lista de avaliações
    else:
        form = EvaluationForm()
    return render(request, 'usuarios/evalProf.html', {'form': form})  

@login_required
@professor_required
def eval_results(request):
    evaluations = Evaluation.objects.filter(evaluator=request.user)
    return render(request, 'usuarios/evalResults.html', {'evaluations': evaluations})

@aluno_required
@login_required
def fill_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    if not evaluation.is_available():
        return render(request, 'usuarios/evalAluno.html', {'evaluation': evaluation, 'is_within_period': False})
    
    if request.method == "POST":
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redireciona após preenchimento
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'usuarios/evalAluno.html', {'form': form, 'evaluation': evaluation, 'is_within_period': True}) 
'''



def p1FACT(request):
    return render(request, 'aluno/p1FACT.html')  # Certifique-se de que o arquivo HTML está na pasta correta

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