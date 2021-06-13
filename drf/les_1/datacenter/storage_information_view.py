from datacenter.models import Visit
from django.shortcuts import render

from project import utils


def storage_information_view(request):
    non_closed_visits = []
    visitors = Visit.objects.filter(leaved_at=None)
    for visitor in visitors:
        current_visit = {
            "who_entered": visitor.passcard.owner_name,
            "entered_at": visitor.entered_at,
            "duration": utils.format_duration(visitor.get_duration()),
        }
        non_closed_visits.append(current_visit)

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
