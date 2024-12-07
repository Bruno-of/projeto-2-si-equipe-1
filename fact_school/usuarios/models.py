from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.contrib.auth import get_user_model

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

    class Meta:
        verbose_name_plural = "Usuários"
    
class Criterion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_score = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Critérios"


class Turma(models.Model):
    name = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turmas')
    alunos = models.ManyToManyField(User, related_name='turmas_inscritas')

    def __str__(self):
        return self.name

class Equipe(models.Model):
    Equipe = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='equipes')
    integrantes = models.ManyToManyField(User, related_name='equipes')
    
    def __str__(self):
        if self.turma:
            return f"{self.Equipe} ({self.turma.name})"
        return f"{self.Equipe} (Sem turma)"

User = get_user_model()
class AvaliacaoFACT(models.Model):
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fact_avaliacoes_feitas', default=None) 
    avaliado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fact_avaliacoes_recebidas', default=None)
    criterio = models.ForeignKey(Criterion, on_delete=models.CASCADE, default=None)
    nota = models.PositiveIntegerField(default=0)
    justificativa = models.TextField(blank = True, null = True, default=None)

    def __call__(self):
        return f"{self.avaliador.username} -> {self.avaliado.username}: {self.criterio.name} ({self.nota})"
    
    class Meta:
        verbose_name_plural = "Avaliações Fact"

class RelatorioAvaliacao(models.Model):
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatorios_avaliacoes_feitas')
    avaliado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatorios_avaliacoes_recebidas')
    criterios_e_notas = models.JSONField()  
    justificativas = models.JSONField()  
    
    def __str__(self):
        return f"Relatório de Avaliação de {self.avaliador.username} para {self.avaliado.username}"
    
    class Meta:
        verbose_name_plural = "Relatórios de Avaliação"
    
    def gerar_relatorio(self):
        # Filtra as avaliações feitas pelo avaliador para o aluno avaliado
        avaliacoes = AvaliacaoFACT.objects.filter(avaliador=self.avaliador, avaliado=self.avaliado)
        criterios_e_notas = []
        justificativas = {}

        # Itera sobre as avaliações para esse par avaliador-avaliado
        for avaliacao in avaliacoes:
            criterios_e_notas.append({
                'criterio': avaliacao.criterio.name,  # Nome do critério
                'nota': avaliacao.nota,  # Nota do critério
            })

            justificativas['justificativa'] = avaliacao.justificativa


        self.criterios_e_notas = criterios_e_notas
        self.justificativas = justificativas
        self.save()


class DisponibilidadeAvaliacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='disponibilidades')
    inicio = models.DateTimeField()
    fim = models.DateTimeField()

    def __str__(self):
        return f"Disponibilidade para {self.turma.name} de {self.inicio} a {self.fim}"
    
    class Meta:
        verbose_name_plural = "Disponibilidades de Avaliação"