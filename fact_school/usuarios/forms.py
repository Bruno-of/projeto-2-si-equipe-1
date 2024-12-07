from django import forms
from usuarios.models import AvaliacaoFACT, Turma, Equipe, Criterion, DisponibilidadeAvaliacao
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()


class DisponibilizarAvaliacaoForm(forms.ModelForm):
    turma = forms.ModelChoiceField(queryset=Turma.objects.all(), required=True, label="Turma")
    inicio = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class':'custom-datetime'}), label="Início da Disponibilidade")
    fim = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local',  'class': 'custom-datetime'}), label="Fim da Disponibilidade")
    class Meta:
        model = DisponibilidadeAvaliacao
        fields = ['turma', 'inicio', 'fim']
    

class ResponderAvaliacaoFACTForm(forms.Form):
    def __init__(self, *args, criterios=None, **kwargs):
        super().__init__(*args, **kwargs)
        if criterios:
            for criterio in criterios:
                self.fields[f'criterio_{criterio.id}'] = forms.IntegerField(
                    #required=True,
                    label=criterio,
                    min_value=0,
                    max_value=criterio.max_score,
                )
        self.fields['justificativa'] = forms.CharField(
            #required=True,
            required=False,
            widget=forms.Textarea,
            label=f'Justificativa',
        )


class CriarAvaliacaoFACTForm(forms.ModelForm):
    def __init__(self, *args, avaliados=None,**kwargs):
        #avaliados = kwargs.pop('avaliados', [])
        super().__init__(*args, **kwargs)
        criterios = Criterion.objects.all()

        for avaliado in avaliados:
            
            for criterio in criterios:
                self.fields[f"nota_{avaliado.id}_{criterio.id}"] = forms.IntegerField(
                    widget=forms.NumberInput(attrs={'min': 0, 'max': criterio.max_score}),
                    label=f"{criterio.name} (Máx: {criterio.max_score} - Avaliando {avaliado.username})",
                    required=True,
                )
            self.fields[f"justificativa_{avaliado.id}"] = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 3}),
                label=f"Justificativa para {avaliado.username}",
                required=True,
            )
    class Meta:
        model = AvaliacaoFACT
        fields = ['avaliador', 'avaliado', 'criterio', 'nota', 'justificativa']

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