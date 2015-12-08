from django.shortcuts import render
from django.http.response import HttpResponse
from iepy.data.models import *
from collections import defaultdict

# Create your views here.
def index(request):
    # entitys = Entity.objects.all()
    docs = IEDocument.objects.all()
    context = {'docs': docs}

    return render(request, 'webapp/index.html', context)


def get_evidence(request, id):
    res = []
    doc = IEDocument.objects.filter(id=id)
    if len(doc) > 0:
        doc = doc[0]
    else:
        return HttpResponse('Invalid ID.')
    evidences = EvidenceCandidate.objects.all()
    # entity_ocurrences = doc.get_entity_occurrences
    segments_id = [x.id for x in doc.get_text_segments()]
    for evidence in evidences:
        if evidence.segment_id in segments_id:
            res.append(evidence)
    context = {'evidences': res}
    return render(request, 'webapp/evidences.html', context)
