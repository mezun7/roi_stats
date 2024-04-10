from django.db.models import Q

from roi.models import Participant

STATUSES = {
    'WIN': 'WIN',
    'PRI': 'PRI',
    '1': 'WIN',
    '2': 'PRI',
    '3': 'PRI',
    'PART': 'PART'
}


def get_hall_of_fame(region=None):
    if region is None:
        participants = Participant.objects.filter()
    else:
        participants = Participant.objects.filter(region=region)

    # participants = participants.filter(~Q(status='PART'))
    results = {

    }

    for participant in participants:
        if participant.student not in results.keys():
            results[participant.student] = {
                'WIN': 0,
                'PRI': 0,
                'PART': 0,
                'OVERALL_RESULTS': 0
            }
        results[participant.student][STATUSES[participant.status]] += 1
    results_ordered = dict(
        sorted(results.items(), key=lambda x: (x[1]['WIN'], x[1]['PRI'], x[1]['PART']), reverse=True))
    return results_ordered
