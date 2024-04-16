from collections import OrderedDict

from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets

from roi.data_structures.participant_result_structure import get_participants_for_html, get_participant_tasks
from roi.halloffame.hall_of_fame import get_hall_of_fame
from roi.models import Olympiad, ParticipantResult, Participant, Region, Task, Student
from roi.serializers import OlympiadSerializer, OlympiadResultSerializer
from roi.templatetags.status_writer import STATUS_CHOICES


# Create your views here.
def main(request):
    olympiads = Olympiad.objects.all().order_by('-date_from')

    results = []

    for olympiad in olympiads:
        participants_count = olympiad.participant_set.count()
        regions_count = Participant.objects.filter(olympiad=olympiad).values_list('region',
                                                                                  flat=True).distinct().count()
        results.append({
            'olympiad': olympiad,
            'participants_count': participants_count,
            'regions_count': regions_count
        })
    context = {
        'results': results
    }
    return render(request, 'roi/main.html', context)


def olympiad_result(request, pk):
    olympiad = Olympiad.objects.get(pk=pk)
    participants = get_participants_for_html(olympiad)
    tasks = olympiad.task_set.all().order_by('day', 'alias')

    context = {
        'participants': participants,
        'olympiad': olympiad,
        'tasks': tasks
    }

    return render(request, 'roi/olymp_raiting.html', context)


def regions_olymp_result(request, olympiad_pk):
    olympiad = Olympiad.objects.get(pk=olympiad_pk)
    participants = Participant.objects.filter(olympiad=olympiad)
    statuses = list(participants.values_list('status', flat=True).distinct().order_by('status'))
    regions = participants.values_list('region__short_name', flat=True).distinct().order_by('region__short_name')
    statuses.append('participants_total')
    statuses.append('total_prizes')
    statuses = sorted(statuses, key=lambda x: STATUS_CHOICES[x][-1])
    regions_results = {

    }
    context = {
        'statuses': statuses,
        'region_results': regions_results,
        'olympiad': olympiad
    }
    for region in regions:
        tmp = {}
        total_prizes = 0
        for status in statuses:
            tmp[status] = 0

        region_participants = participants.filter(region__short_name=region)
        participants_total = region_participants.count()

        for participant in region_participants:
            tmp[participant.status] += 1

        for key, value in tmp.items():
            if key != 'PART':
                total_prizes += value

        tmp['participants_total'] = participants_total
        tmp['total_prizes'] = total_prizes
        regions_results[region] = tmp

    return render(request, 'roi/region_olymp_result.html', context=context)


def region_results_view(request, region_pk):
    region = Region.objects.get(pk=region_pk)
    participants = Participant.objects.filter(region=region).order_by('rank')

    results = {}

    tasks = {}

    for olympiad in Olympiad.objects.all().order_by('-date_from'):
        tasks[olympiad.date_to.year] = ['.' for _ in Task.objects.filter(olympiad=olympiad).order_by('alias')]

    for participant in participants:
        year = participant.olympiad.date_from.year
        if year not in results:
            results[year] = {
                'rowspans': participants.filter(olympiad__date_from__year=year).count(),
                'results': []
            }
        participant_tasks = tasks[participant.olympiad.date_from.year][:]
        for ind, participant_result in enumerate(participant.participantresult_set.all().order_by('task__alias')):
            participant_tasks[ind] = participant_result.score
        results[year]['results'].append(
            {
                'tasks': participant_tasks,
                'participant': participant
            }
        )
    context = {
        'region': region,
        'results': results
    }
    return render(request, 'roi/region_result.html', context=context)


def region_delegetaions_view(request, region_pk):
    region = Region.objects.get(pk=region_pk)

    olympiads = Olympiad.objects.all().order_by('-date_to')
    results = []

    for olympiad in olympiads:
        year = olympiad.date_to.year
        participants = Participant.objects.filter(olympiad=olympiad, region=region)
        winners = participants.filter(Q(status='WIN') | Q(status='1')).count()
        prizes = participants.filter(Q(status='PRI') | Q(status='2') | Q(status='3')).count()
        overall_participants = participants.count()
        overall_results = winners + prizes
        results.append([year, overall_participants, winners, prizes, overall_results])

    context = {
        'region': region,
        'results': results
    }
    return render(request, 'roi/region_delegation.html', context)


def student_view(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    participants = Participant.objects.filter(student=student).order_by('-olympiad__date_to__year')
    res = []
    for participant in participants:
        res.append({
            'participant': participant,
            'tasks': get_participant_tasks(participant)
        })
    context = {
        'results': res,
        'student': student
    }
    return render(request, 'roi/student_template.html', context)


def region_hall_of_fame(request, region_pk=None):
    region = None
    if region_pk is not None:
        region = Region.objects.get(pk=region_pk)
    hall_of_fame = get_hall_of_fame(region)
    context = {'region': region,
               'results': hall_of_fame}
    return render(request, 'roi/hall_of_fame_region.html', context)


def region_view(request, region_pk):
    region = Region.objects.get(pk=region_pk)
    participants = Participant.objects.filter(region=region)
    try:
        first_year_of_participations = (participants.
                                        order_by('olympiad__date_from').
                                        first().
                                        olympiad.date_from.year)

    except AttributeError:
        first_year_of_participations = '0'

    overall_contestants = len(participants)
    winners = len(participants.filter(Q(status='WIN') | Q(status='1')))
    prizes = len(participants.filter(Q(status='PRI') | Q(status='2') | Q(status='3')))
    context = {
        'region': region,
        'first_year_of_participations': first_year_of_participations,
        'overall_contestants': overall_contestants,
        'winners': winners,
        'prizes': prizes
    }
    return render(request, 'roi/region_main.html', context=context)


def regions_results(request):
    regions = Region.objects.all().order_by('short_name')
    results = []
    for region in regions:
        WIN = Participant.objects.filter(region=region).filter(Q(status='WIN') | Q(status='1')).count()
        PRI = Participant.objects.filter(region=region).filter(Q(status='PRI') | Q(status='2') | Q(status='3')).count()
        total = WIN + PRI
        res = {
            'region': region,
            'host': Olympiad.objects.filter(region=region),
            'WIN': WIN,
            'PRI': PRI,
            'total': total
        }
        results.append(res)
    context = {
        'results': results
    }
    return render(request, 'roi/regions_results.html', context)


def fix_patranomic(request):
    participants = Participant.objects.filter(student__patranomic='', grade__isnull=False).order_by('olympiad__date_from__year')
    students = []
    for participant in participants:
        participants_with_patronomic = (Participant.objects.
                                        filter(student__name=participant.student.name,
                                               student__surname=participant.student.surname,
                                               grade__isnull=False).
                                        exclude(student__patranomic='').order_by('student__surname', 'student__name'))
        for prt in participants_with_patronomic:
            if abs(prt.olympiad.date_from.year - participant.olympiad.date_from.year) == abs(prt.grade - participant.grade):
                participant.student = prt.student
                participant.save()
                print(prt, prt.grade, prt.olympiad.date_from.year, '->', participant, participant.grade, participant.olympiad.date_from.year)
                break
        if len(participants_with_patronomic) > 0:
            print('------')
    # print(students)
