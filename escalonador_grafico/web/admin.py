from django.contrib import admin
from .models import *
from django.urls import path, include
from django.http import HttpResponseRedirect


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    pass


@admin.register(Dia)
class DiaAdmin(admin.ModelAdmin):
    pass


class DiaEmProfessorInline(admin.TabularInline):
    model = DiaEmProfessor
    extra = 1
    raw_id_fields = ("dia",)


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    inlines = (DiaEmProfessorInline,)


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    pass


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    pass


class ProfessorEmTurmaInline(admin.TabularInline):
    model = ProfessorEmTurma
    extra = 1
    raw_id_fields = ("professor",)


class GrupoEmTurmaInline(admin.TabularInline):
    model = GrupoEmTurma
    extra = 1
    raw_id_fields = ("grupo",)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'get_professor', 'disciplina', 'periodo','dias')
    readonly_fields = ('dias',)
    inlines = (ProfessorEmTurmaInline, GrupoEmTurmaInline)
    change_list_template = 'turma_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dia/', self.set_dia)
        ]
        return custom_urls + urls

    def set_dia(self, request):
        if 'apply' in request.POST:
            for turma in Turma.objects.all():
                for professor in Professor.objects.filter(professoremturma__turma=turma):
                    for dia in Dia.objects.filter(diaemprofessor__professor=professor):
                        grupo = []
                        for grupos in turma.grupo.all():
                            for turma_do_grupo in Turma.objects.filter(grupoemturma__grupo=grupos, dias=dia):
                                grupo.append(turma_do_grupo)
                        if len(Turma.objects.filter(professoremturma__professor=professor, dias=dia)) < 1 \
                                and len(
                            Turma.objects.filter(professoremturma__professor=professor, disciplina=turma.disciplina,
                                                 dias=dia)) < 1 \
                                and len(Turma.objects.filter(periodo=turma.periodo, dias=dia)) < 1 and len(grupo) < 1:
                            mesma_disciplina_professores_diferentes = Turma.objects.filter(disciplina=turma.disciplina)[0]
                            if mesma_disciplina_professores_diferentes and \
                                    mesma_disciplina_professores_diferentes.dias != None:
                                turma.dias = mesma_disciplina_professores_diferentes.dias
                            else:
                                turma.dias = dia
                            turma.save()
            return HttpResponseRedirect("../")
