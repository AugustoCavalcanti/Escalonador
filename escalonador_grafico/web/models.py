from django.db import models

class Dia(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Professor(models.Model):
    nome = models.CharField(max_length=128)
    dias_livres = models.ManyToManyField(Dia)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=128)

    def __str__(self):
        return self.nome


class Periodo(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Turma(models.Model):
    nome = models.CharField(max_length=128, null=True, blank=True)
    disciplina = models.ManyToManyField(Disciplina, through='DisciplinaEmTurma')
    periodo = models.ManyToManyField(Periodo, through='PeriodoEmTurma')
    dia = models.CharField(max_length=128, blank=True, null=True)
    professor = models.ManyToManyField(Professor, through='ProfessorEmTurma')

    def __str__(self):
        return self.nome

class ProfessorEmTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.turma.nome
        except AttributeError:
            return self.turma


class DisciplinaEmTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.turma.nome
        except AttributeError:
            return self.turma


class PeriodoEmTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.turma.nome
        except AttributeError:
            return self.turma