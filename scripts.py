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
        print('Все плохие оценки для "{}" исправлены на 5'.format(schoolkid.full_name))
    except ObjectDoesNotExist:
        print('Введено имя:', schoolkid_name, '- Ученика с таким ФИО нет в базе.\nИсправте ФИО и повторите попытку')
    except MultipleObjectsReturned:
        print('Введено имя:', schoolkid_name, '- С таким ФИО найдено больше 1ого ученика.\nИсправте ФИО и повторите попытку')


def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        schoolkid_chastisements.delete()
        print('Все замечания для "{}" удалены'.format(schoolkid.full_name))
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
                commendation_text = random.choice(commendations_text)
                Commendation.objects.create(text=commendation_text, created=lesson.date, schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
                print('Создана похвала: "{}" - по предмету "{}" для "{}"'.format(commendation_text, subject_name, schoolkid.full_name))
                return
    except ObjectDoesNotExist:
        print('Введено имя:', schoolkid_name, '- Ученика с таким ФИО нет в базе.\nИсправте ФИО и повторите попытку')
    except MultipleObjectsReturned:
        print('Введено имя:', schoolkid_name, '- С таким ФИО найдено больше 1ого ученика.\nИсправте ФИО и повторите попытку')
