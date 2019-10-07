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


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    pass


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


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    inlines = (ProfessorEmTurmaInline, DisciplinaEmTurmaInline, PeriodoEmTurmaInline)
    change_list_template = 'turma_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dia/', self.set_dia)
        ]
        return custom_urls + urls

    def set_dia(self):
        pass
