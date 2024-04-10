import codecs
import csv
from datetime import datetime

from roi.models import Olympiad, Task, Student, Region, RegionAlias, Participant, ParticipantResult


def get_status(status):
    statuses = {
        'победитель': 'WIN',
        'призер': 'PRI',
        '1': '1',
        '2': '2',
        '3': '3',
        '': 'PART'
    }
    return statuses[status.lower()]


def get_student(surname, name, patranomic):
    surname = surname.strip()
    name = name.strip()
    patranomic = patranomic.strip()
    try:
        student = Student.objects.get(surname__iexact=surname, name__iexact=name, patranomic__iexact=patranomic)
    except Student.DoesNotExist:
        student = Student()
        student.surname = surname
        student.name = name
        student.patranomic = patranomic
        student.save()

    return student


def get_region(reg):
    region = None
    try:
        region = Region.objects.get(short_name__iexact=reg.strip())
    except Region.DoesNotExist:
        try:
            region = RegionAlias.objects.get(alias__iexact=reg.strip()).region
        except RegionAlias.DoesNotExist:
            print(f"No such region - {reg}")
    return region


def create_tasks(olympiad: Olympiad, tasks: []):
    print("Creating tasks")
    tasks_map = {}
    for t_ind, task in enumerate(tasks):
        print(task)
        alias, name, day = tuple(task.split('&'))
        max_score = 100
        try:
            model_task = Task.objects.get(alias=alias, olympiad=olympiad)
            model_task.name = name
            model_task.olympiad = olympiad
            model_task.alias = alias
            model_task.save()
        except Task.DoesNotExist:
            model_task = Task(name=name, olympiad=olympiad, alias=alias, day=day, max_score=max_score)
            model_task.save()
        tasks_map[t_ind] = model_task
    return tasks_map


def import_olympiad_results(csv_file, olympiad: Olympiad):
    reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
    header_tasks = None
    for index, row in enumerate(reader):
        tasks = row[6:len(row) - 2]
        if index == 0:
            header_tasks = create_tasks(olympiad, tasks[:])
            continue

        student = get_student(row[1], row[2], row[3])
        region = get_region(row[4])
        try:
            grade = int(row[5])
        except ValueError:
            grade = None
        score = int(row[-2])
        rank = int(row[0])
        try:
            participant = Participant.objects.get(student=student, olympiad=olympiad)
        except Participant.DoesNotExist:
            participant = Participant()
        participant.student = student
        participant.region = region
        participant.grade = grade
        participant.score = score
        participant.rank = rank
        participant.status = get_status(row[-1])
        participant.olympiad = olympiad
        participant.save()
        for t_ind, task in enumerate(tasks):
            if not task.isnumeric():
                continue
            task_model = header_tasks[t_ind]
            try:
                participant_result = ParticipantResult.objects.get(participant=participant, task=task_model)
            except ParticipantResult.DoesNotExist:
                participant_result = ParticipantResult()
            participant_result.participant = participant
            participant_result.task = task_model
            participant_result.score = int(task)
            participant_result.save()


def get_date(date_str):
    return datetime.strptime(date_str, '%d.%m.%Y').date()


def import_olympiads(olympiad_file):
    reader = csv.reader(codecs.iterdecode(olympiad_file, 'utf-8'))

    for ind, row in enumerate(reader):
        if ind == 0:
            continue
        olympiad = Olympiad()
        olympiad.name = row[0]
        olympiad.date_from = get_date(row[1])
        olympiad.date_to = get_date(row[2])
        olympiad.region = get_region(row[3])
        olympiad.city = row[4]
        olympiad.olymp_site = row[5]
        olympiad.codeforces_tour = row[6]
        olympiad.save()
