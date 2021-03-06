from django.db import models


class Dia(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    nome = models.CharField(max_length=128)
    dias_livres = models.ManyToManyField(Dia, through='DiaEmProfessor')

    def __str__(self):
        return self.nome


class DiaEmProfessor(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
    dia = models.ForeignKey(Dia, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.dia.nome
        except AttributeError:
            return self.dia


class Disciplina(models.Model):
    nome = models.CharField(max_length=128)

    def __str__(self):
        return self.nome


class Periodo(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Grupo(models.Model):
    nome = models.CharField(max_length=128)

    def __str__(self):
        return self.nome


class Turma(models.Model):
    nome = models.CharField(max_length=128, null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.SET_NULL, null=True)
    dias = models.ForeignKey(Dia,  on_delete=models.SET_NULL, null=True, blank=True)
    professor = models.ManyToManyField(Professor, through='ProfessorEmTurma')
    grupo = models.ManyToManyField(Grupo, through='GrupoEmTurma', blank=True)

    def get_professor(self):
        return ",".join([str(professor) for professor in Professor.objects.filter(professoremturma__turma=self)])

    def __str__(self):
        return self.nome


class ProfessorEmTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.professor.nome
        except AttributeError:
            return self.professor


class GrupoEmTurma(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.grupo.nome
        except AttributeError:
            return self.grupo


# class DiaEmTurma(models.Model):
#     turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
#     dia = models.ForeignKey(Dia, on_delete=models.SET_NULL, null=True)
#
#     def __str__(self):
#         try:
#             return self.dia.nome
#         except AttributeError:
#             return self.dia