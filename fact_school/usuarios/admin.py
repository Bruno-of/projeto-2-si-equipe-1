from django.contrib import admin
from .models import Turma, User, Criterion, AvaliacaoFACT
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'max_score')  
    search_fields = ('name',) 


User = get_user_model()

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Adiciona o usuário automaticamente ao grupo "Professores" ao salvar
        if not obj.groups.filter(name="Professores").exists():
            professor_group, created = Group.objects.get_or_create(name="Professores")
            obj.groups.add(professor_group)

from django.contrib import admin
from .models import Turma

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('name', 'professor')
    list_filter = ('professor',)
    search_fields = ('name',)
    
    # Usando filter_horizontal para a relação ManyToMany com os alunos
    filter_horizontal = ('alunos',)  # Mostra uma interface mais amigável para adicionar/remover alunos
    
    # Se você preferir usar raw_id_fields (menor lista de alunos):
    # raw_id_fields = ('professor', 'alunos')  # Só para quando houver muitos alunos e você não quer a lista suspensa grande


admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from .models import RelatorioAvaliacao

class RelatorioAvaliacaoAdmin(admin.ModelAdmin):
    # Defina os campos que você quer exibir no admin
    list_display = ('avaliador', 'avaliado', 'get_criterios_e_notas')
    search_fields = ('avaliador__username', 'avaliado__username')  # Permite buscar por nome do avaliador ou avaliado
    
    # Método para exibir os critérios e notas no admin de forma legível
    def get_criterios_e_notas(self, obj):
        # Exibe os critérios e notas de forma legível no admin
        return ", ".join([f"{item['criterio']}: {item['nota']}" for item in obj.criterios_e_notas])
    get_criterios_e_notas.short_description = "Critérios e Notas"  # Customiza o nome da coluna

# Registra o modelo e o admin customizado
admin.site.register(RelatorioAvaliacao, RelatorioAvaliacaoAdmin)


class AvaliacaoFACTAdmin(admin.ModelAdmin):
    list_display = ('avaliador', 'avaliado', 'criterio', 'nota', 'justificativa')
    search_fields = ('avaliador__username', 'avaliado__username', 'criterio__name')
    list_filter = ('criterio', 'nota')

admin.site.register(AvaliacaoFACT, AvaliacaoFACTAdmin)


from django.contrib import admin
from .models import DisponibilidadeAvaliacao

class DisponibilidadeAvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('turma', 'inicio', 'fim')
    search_fields = ('turma__name',)
    list_filter = ('turma', 'inicio', 'fim')

admin.site.register(DisponibilidadeAvaliacao, DisponibilidadeAvaliacaoAdmin)