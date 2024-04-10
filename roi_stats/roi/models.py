from django.db import models

# Create your models here.

STATUS_CHOICES = (
    ('WIN', 'Победитель'),
    ('PRI', 'Призер'),
    ('1', 'Диплом 1 степени'),
    ('2', 'Диплом 2 степени'),
    ("3", "Диплом 3 степени"),
    ('PART', 'Участник')
)


class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    patranomic = models.CharField(max_length=100, null=True, blank=True, verbose_name='Отчество')

    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.patranomic)

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = "Ученики"


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name='Полное название региона')
    short_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Короткое название региона')
    region_code = models.IntegerField(verbose_name='Код региона', null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Регион существует?')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = "Регионы"


class RegionAlias(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.region} -> {self.alias}'


class Olympiad(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название олимпиады')
    date_from = models.DateField(verbose_name='Дата начала олимпиады')
    date_to = models.DateField(verbose_name='Дата окончания олимпиады')
    region = models.ForeignKey(Region, verbose_name='Регион', on_delete=models.CASCADE)
    city = models.CharField(max_length=100, verbose_name='Город')
    olymp_site = models.URLField(null=True, blank=True, verbose_name='Сайт олимпиады')
    codeforces_tour = models.URLField(null=True, blank=True, verbose_name='Codeforces тур')

    def __str__(self):
        return f'{self.date_from.year}-{self.name}'

    class Meta:
        verbose_name = 'Олимпиада'
        verbose_name_plural = 'Олимпиады'


class Task(models.Model):
    alias = models.CharField(max_length=100, verbose_name='Короткое название')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название')
    olympiad = models.ForeignKey(Olympiad, verbose_name='Олимпиада', on_delete=models.CASCADE)
    day = models.CharField(max_length=100, null=True, blank=True, verbose_name='День')
    max_score = models.IntegerField(default=100, verbose_name='Максимальный балл за задачу')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Participant(models.Model):
    student = models.ForeignKey(Student, verbose_name='Участник', on_delete=models.CASCADE)
    olympiad = models.ForeignKey(Olympiad, verbose_name='Олимпиада', on_delete=models.CASCADE)
    region = models.ForeignKey(Region, verbose_name='Регион', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, verbose_name='Статус', choices=STATUS_CHOICES)
    grade = models.IntegerField(verbose_name='Класс', null=True, blank=True)
    rank = models.IntegerField(verbose_name='Место', null=True, blank=True)
    score = models.IntegerField(verbose_name='Итоговый балл', null=True, blank=True)

    def __str__(self):
        return str(self.student)

    class Meta:
        verbose_name = 'Участник олимпиады'
        verbose_name_plural = 'Участники олимпиады'


class ParticipantResult(models.Model):
    participant = models.ForeignKey(Participant, verbose_name='Участник', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name='Балл')

    class Meta:
        verbose_name = 'Результат участника'
        verbose_name_plural = 'Результаты участников'
