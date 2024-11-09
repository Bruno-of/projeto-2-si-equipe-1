from django import forms
from usuarios.models import Evaluation
from django.contrib.auth.models import User

class EvaluationForm(forms.ModelForm):
    evaluated = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Seleciona todos os usuários (alunos)
        widget=forms.CheckboxSelectMultiple,  # Permite múltiplas seleções
        label="Selecionar Alunos"
    )
    class Meta:
        model = Evaluation
        fields = ['evaluated', 'criterion', 'start_date', 'end_date']


class EvaluationResponseForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['score', 'justification']
