from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    is_adm = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Define um nome único para o reverso
        blank=True,
        help_text='Os grupos a que este usuário pertence.',
        verbose_name='grupos'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Define um nome único para o reverso
        blank=True,
        help_text='Permissões específicas para este usuário.',
        verbose_name='permissões de usuário'
    )
    
class Criterion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_score = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name
'''
class Category(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name="categories")
    min_score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.criterion.name}: {self.min_score}-{self.max_score}%"

class Evaluation(models.Model):
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_given')
    evaluated = models.ManyToManyField(User, related_name='evaluations_received')
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    justification = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField() 

    def is_available(self):
        return self.start_date <= now() <= self.end_date

    def __str__(self):
        return f"{self.evaluator} -> {self.evaluated} ({self.criterion.name})"
'''

class Turma(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turmas')
    alunos = models.ManyToManyField(User, related_name='turmas_inscritas')

    def __str__(self):
        return self.name

class Equipe(models.Model):
    Equipe = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='equipes', default=None)
    integrantes = models.ManyToManyField(User, related_name='equipes')
    
    def __str__(self):
        return f"{self.nome} ({self.turma.name})"

class AvaliacaoFACT(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, default=None) 
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, null = True, blank = True)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()

    def esta_disponivel(self):
        return self.inicio <= now() <= self.fim

class RespostaFACT(models.Model):
    avaliacao = models.ForeignKey(AvaliacaoFACT, on_delete=models.CASCADE, related_name='respostas')
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respostas_dadas')
    avaliado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respostas_recebidas')
    criterio = models.CharField(max_length=100)
    nota = models.PositiveIntegerField()
    justificativa = models.TextField(blank = True, null = True)