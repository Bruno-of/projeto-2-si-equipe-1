from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.custom_login, name='login'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('avaliacao/evalProf/', views.make_available, name='evalProf'),
    path('professor_home/', views.professor_home, name='professor_home'),
    path('aluno_home/', views.aluno_home, name='aluno_home'),
    #path('configurar_fact/', views.configurar_avaliacao_fact, name='configurar_fact'),
    path('responder_fact/<int:equipe_id>/', views.responder_fact, name='responder_fact'),
    path('criar_equipe/', views.criar_equipe, name='criar_equipe'),
    path('visualizar_avaliacoes/<int:turma_id>/', views.visualizar_avaliacoes, name='visualizar_avaliacoes'),
    path('listar_e_excluir_equipes/', views.listar_e_excluir_equipes, name='listar_e_excluir_equipes'),
    path('verFACT/', views.verFACT, name='verFACT'),
    path('equipe/', views.equipe, name='equipe'),

]
