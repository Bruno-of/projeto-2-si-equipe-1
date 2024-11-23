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
    description = models.TextField(default=0)
    max_score = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name

class Category(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name="categories", default=1)
    min_score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=20)
    description = models.TextField()

    def __str__(self):
        return f"{self.criterion.name}: {self.min_score}-{self.max_score}%"

class Evaluation(models.Model):
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_given')
    evaluated = models.ManyToManyField(User, related_name='evaluations_received')
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=10)
    justification = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField() 

    def is_available(self):
        return self.start_date <= now() <= self.end_date

    def __str__(self):
        return f"{self.evaluator} -> {self.evaluated} ({self.criterion.name})"
    
class Turma(models.Model):
        name = models.CharField(max_length=100, unique=True)

        def __str__(self):
            return self.name
       
class Grupo(models.Model):
    name = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="grupos")

    def __str__(self):
        return f"{self.name} ({self.turma.name})"
    
class Aluno(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="alunos")

    def __str__(self):
        return f"{self.name} - {self.grupo.name} ({self.grupo.turma.name})"
    

