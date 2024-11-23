from django.contrib import admin
from .models import Criterion, Category, Evaluation, Turma, Grupo, Aluno
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'max_score')  
    search_fields = ('name',) 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('criterion', 'min_score', 'max_score', 'description')  
    list_filter = ('criterion',)
    search_fields = ('criterion',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('evaluator', 'criterion', 'get_evaluated', 'start_date', 'end_date', 'is_available')
    list_filter = ('evaluator', 'criterion')
    search_fields = ('evaluator__username', 'evaluated__username', 'criterion__name')

    def get_evaluated(self, obj):
        return ', '.join([user.username for user in obj.evaluated.all()])
    get_evaluated.short_description = 'Avaliados'


User = get_user_model()

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Adiciona o usuário automaticamente ao grupo "Professores" ao salvar
        if not obj.groups.filter(name="Professores").exists():
            professor_group, created = Group.objects.get_or_create(name="Professores")
            obj.groups.add(professor_group)

admin.site.unregister(User) 
admin.site.register(User, CustomUserAdmin) 

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('name', 'turma')
    list_filter = ('turma',)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'grupo')
    list_filter = ('grupo', 'grupo__turma')
    search_fields = ('name', 'email')