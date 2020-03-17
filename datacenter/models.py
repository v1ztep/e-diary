from django.db import models

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Lesson, Schoolkid, Chastisement, Mark, Commendation
import random


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        schoolkid_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
        for mark in schoolkid_marks:
            mark.points = 5
            mark.save()
    except ObjectDoesNotExist:
        print('Введено имя:', schoolkid_name, '- Ученика с таким ФИО нет в базе.\nИсправте ФИО и повторите попытку')
    except MultipleObjectsReturned:
        print('Введено имя:', schoolkid_name, '- С таким ФИО найдено больше 1ого ученика.\nИсправте ФИО и повторите попытку')


def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        schoolkid_chastisements.delete()
    except ObjectDoesNotExist:
        print('Введено имя:', schoolkid_name, '- Ученика с таким ФИО нет в базе.\nИсправте ФИО и повторите попытку')
    except MultipleObjectsReturned:
        print('Введено имя:', schoolkid_name, '- С таким ФИО найдено больше 1ого ученика.\nИсправте ФИО и повторите попытку')


def create_commendation(schoolkid_name, subject_name):
    commendations_text = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                          'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
                          'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!',
                          'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                          'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
                          'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
                          'Это как раз то, что нужно!', 'Я тобой горжусь!',
                          'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
                          'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                          'Теперь у тебя точно все получится!']
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject__title=subject_name).order_by('-date')
        for lesson in lessons:
            presence_commendation = Commendation.objects.filter(created=lesson.date, schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
            if len(presence_commendation) < 1:
                Commendation.objects.create(text=random.choice(commendations_text), created=lesson.date, schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
                return
    except ObjectDoesNotExist:
        print('Введено имя:', schoolkid_name, '- Ученика с таким ФИО нет в базе.\nИсправте ФИО и повторите попытку')
    except MultipleObjectsReturned:
        print('Введено имя:', schoolkid_name, '- С таким ФИО найдено больше 1ого ученика.\nИсправте ФИО и повторите попытку')


class Schoolkid(models.Model):
    """Ученик"""
    full_name = models.CharField('ФИО', max_length=200)
    birthday = models.DateField('день рождения', null=True)

    entry_year = models.IntegerField('год начала обучения', null=True)
    year_of_study = models.IntegerField('год обучения', null=True)
    group_letter = models.CharField('литера класса', max_length=1, null=True)

    def __str__(self):
        return f"{self.full_name} {self.year_of_study}{self.group_letter}"


class Teacher(models.Model):
    """Учитель"""
    full_name = models.CharField('ФИО', max_length=200)
    birthday = models.DateField('день рождения', null=True)

    def __str__(self):
        return f"{self.full_name}"


class Subject(models.Model):
    """Предмет: математика, русский язык и пр. — привязан к году обучения."""
    title = models.CharField('название', max_length=200)
    year_of_study = models.IntegerField('год обучения', null=True, db_index=True)

    def __str__(self):
        return f"{self.title} {self.year_of_study} класса"


class Lesson(models.Model):
    """Один урок в расписании занятий."""

    TIMESLOTS_SCHEDULE = [
        "8:00-8:40",
        "8:50-9:30",
        "9:40-10:20",
        "10:35-11:15",
        "11:25-12:05"
    ]

    year_of_study = models.IntegerField(db_index=True)
    group_letter = models.CharField('литера класса', max_length=1, db_index=True)

    subject = models.ForeignKey(Subject, null=True, verbose_name='предмет', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, null=True, verbose_name='учитель', on_delete=models.CASCADE)

    timeslot = models.IntegerField('слот', db_index=True, help_text='Номер слота в расписании уроков на этот день.')
    room = models.CharField('класс', db_index=True, help_text='Класс где проходят занятия.', max_length=50)
    date = models.DateField('дата', db_index=True)

    def __str__(self):
        return f"{self.subject.title} {self.year_of_study}{self.group_letter}"


class Mark(models.Model):
    """Оценка, поставленная учителем ученику."""
    points = models.IntegerField('оценка')
    teacher_note = models.TextField('комментарий', null=True)
    created = models.DateField('дата')
    schoolkid = models.ForeignKey(Schoolkid, verbose_name='ученик', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name='предмет', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name='учитель', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.points} {self.schoolkid.full_name}"


class Chastisement(models.Model):
    """Запись с замачанием от учителя ученику."""
    text = models.TextField('замечание')
    created = models.DateField('дата', db_index=True)
    schoolkid = models.ForeignKey(Schoolkid, verbose_name='ученик', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name='предмет', null=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey(Teacher, verbose_name='учитель', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.schoolkid.full_name}"


class Commendation(models.Model):
    """Запись с похвалой от учителя ученику."""
    text = models.TextField('похвала')
    created = models.DateField('дата', db_index=True)
    schoolkid = models.ForeignKey(Schoolkid, verbose_name='ученик', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name='предмет', null=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey(Teacher, verbose_name='учитель', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.schoolkid.full_name}"
