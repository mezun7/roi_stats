from typing import List

from roi.models import Olympiad, Participant, Task, ParticipantResult


def get_participant_tasks(participant: Participant, tasks=None):
    if tasks is None:
        tasks = participant.olympiad.task_set.all().order_by('alias')
    participant_results = ParticipantResult.objects.filter(participant=participant).order_by('task__alias')
    tasks_results = [{'result': '.'} for task in tasks]
    tasks = [task.alias for task in tasks]
    for pr in participant_results:
        ind = tasks.index(pr.task.alias)
        tasks_results[ind]['result'] = pr.score
    return tasks_results


def get_participants_for_html(olympiad: Olympiad):
    participants = Participant.objects.filter(olympiad=olympiad).order_by('rank')
    tasks = Task.objects.filter(olympiad=olympiad).order_by('day', 'alias')
    result = []

    for participant in participants:
        tmp = {
            'participant': participant,
            'tasks': get_participant_tasks(participant, tasks)
        }
        result.append(tmp)
    return result
