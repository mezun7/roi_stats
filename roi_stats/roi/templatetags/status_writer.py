from django import template

from roi.models import Participant

register = template.Library()
STATUS_CHOICES = {
    'WIN': ['Победитель', 'table-warning', 0],
    'PRI': ['Призер', 'table-info', 1],
    '1': ['Диплом 1 степени', 'table-warning', 0],
    '2': ['Диплом 2 степени', 'table-info', 1],
    "3": ["Диплом 3 степени", 'bg-orange', 2],
    'PART': ['', '', 3],
    'participants_total': ['Общее количество участников', 4],
    'total_prizes': ['Общее количество призовых мест', 5],
    '': ['', '', 3],
}


@register.filter()
def get_status(status):
    return STATUS_CHOICES[status][0]


@register.filter()
def get_class(participant: Participant):
    return STATUS_CHOICES[participant.status][-2]


@register.filter()
def get_overall_participations(result):
    return result['WIN'] + result['PRI'] + result['PART']


@register.filter()
def get_overall_results(result):
    return result['WIN'] + result['PRI']
