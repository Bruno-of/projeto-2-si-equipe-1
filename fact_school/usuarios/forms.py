from django import forms
from usuarios.models import AvaliacaoFACT, Turma, Equipe
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()
'''
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
'''

class CriarAvaliacaoFACTForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoFACT
        fields = ['turma', 'equipe', 'inicio', 'fim']

class ResponderAvaliacaoFACTForm(forms.Form):
    def __init__(self, *args, criterios=None, **kwargs):
        super().__init__(*args, **kwargs)
        if criterios:
            for criterio in criterios:
                self.fields[f'criterio_{criterio.id}'] = forms.IntegerField(
                    label=criterio,
                    min_value=0,
                    max_value=criterio.max_score,
                )
                self.fields[f'justificativa_{criterio.id}'] = forms.CharField(
                    required=False,
                    widget=forms.Textarea,
                    label=f'Justificativa para {criterio}',
                )

alunos_grupo = User.objects.filter(groups__name='alunos')


class CriarEquipeForm(forms.ModelForm):
    alunos = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'turma' in self.data:
            try:
                turma_id = int(self.data.get('turma'))
                self.fields['alunos'].queryset =User.objects.filter(turmas_inscritas__id=turma_id, groups__name='Alunos').distinct()

            except (ValueError, TypeError):
                self.fields['alunos'].queryset = User.objects.none()
        elif self.instance.pk:
            self.fields['alunos'].queryset = self.instance.turma.alunos.filter(groups__name='alunos').distinct()
    class Meta:
        model = Equipe
        fields = ['Equipe', 'turma', 'alunos']

    def save(self, commit=True):
        equipe = super().save(commit=False)
        if commit:
            equipe.save()
            self.save_m2m()
            equipe.integrantes.set(self.cleaned_data['alunos'])
        return equipe
    