from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render

from project import utils


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = Passcard.objects.get(passcode=passcode)
    for visit in Visit.objects.filter(passcard=passcard):
        visit_info = {
            "entered_at": visit.entered_at,
            "duration": utils.format_duration(visit.get_duration()),
            "is_strange": visit.is_visit_long()
        }
        this_passcard_visits.append(visit_info)
    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
