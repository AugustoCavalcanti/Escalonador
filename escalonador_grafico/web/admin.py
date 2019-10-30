from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from .models import *
from dynamic_raw_id.admin import DynamicRawIDMixin
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
    raw_id_fields = ('dia',)


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    inlines = (DiaEmProfessorInline,)


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    pass


class ProfessorEmTurmaInline(admin.TabularInline):
    model = ProfessorEmTurma
    extra = 1
    raw_id_fields = ('professor',)


class DisciplinaEmTurmaInline(admin.TabularInline):
    model = DisciplinaEmTurma
    extra = 1
    raw_id_fields = ('disciplina',)


class PeriodoEmTurmaInline(admin.TabularInline):
    model = PeriodoEmTurma
    extra = 1
    raw_id_fields = ('periodo',)


class GrupoEmTurmaInline(admin.TabularInline):
    model = GrupoEmTurma
    extra = 1
    raw_id_fields = ('grupo',)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'dia')
    inlines = (ProfessorEmTurmaInline, DisciplinaEmTurmaInline, PeriodoEmTurmaInline, GrupoEmTurmaInline)
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
                        disciplina = Disciplina.objects.filter(disciplinaemturma__turma=turma)[0]
                        periodo = Periodo.objects.filter(periodoemturma__turma=turma)[0]
                        grupo = Grupo.objects.filter(grupoemturma__turma=turma)[0]
                        if len(Turma.objects.filter(professoremturma__professor=professor, dia=dia)) < 1 and len(Turma.objects.filter(disciplinaemturma__disciplina=disciplina, dia=dia)) < 1 and len(Turma.objects.filter(periodoemturma__periodo=periodo, dia=dia)) < 1 and len(Turma.objects.filter(grupoemturma__grupo=grupo, dia=dia)) < 1:
                            turma.dia = dia
                            turma.save()
            return HttpResponseRedirect("../")