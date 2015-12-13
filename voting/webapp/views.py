from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from iepy.data.models import *
from voting.webapp.models import *
from collections import defaultdict
import random


# Create your views here.
def index(request):
    # entitys = Entity.objects.all()
    docs = IEDocument.objects.all()
    context = {'docs': docs}

    return render(request, 'webapp/index.html', context)


def question(request):
    if not request.user.is_authenticated():
        return HttpResponse('Necesitas estar loggeado.')

    # generar la pregunta y llamar a save_choice
    user = User.objects.get(id=request.user.id)
    choices = Choice.objects.filter(user=user)
    questions_ans = [x.question for x in choices]
    questions = [x for x in Question.objects.all() if x not in questions_ans]
    if len(questions) <= 0:
        return HttpResponse('Ya respondiste todas las preguntas.')

    selected = random.choice(questions)

    context = {'question': selected}
    return render(request, 'webapp/question.html', context)


def save_choice(request):
    if not request.user.is_authenticated():
        return HttpResponse('Necesitas estar loggeado.')

    user = User.objects.filter(id=request.user.id)[0]
    if request.method == 'POST':
        # guardar las Choices con lo que responda el usuario
        id_question = request.POST['id_question']
        question = Question.objects.get(id=id_question)
        choice = request.POST['choice']
        if choice == '1':
            vote = Vote.objects.get(vote='AFIRMATIVO')
        elif choice == '0':
            vote = Vote.objects.get(vote='NEGATIVO')
        else:
            vote = Vote.objects.get(vote='INDIFERENTE')

        ch = Choice()
        ch.user = user
        ch.question = question
        ch.choice = vote
        ch.save()
        return redirect('/webapp/question')

    return HttpResponse('Acceso ilegal')


def results(request):
    if not request.user.is_authenticated():
        return HttpResponse('Necesitas estar loggeado.')
    counts = defaultdict(int)
    user = User.objects.get(id=request.user.id)
    laws = Law.objects.all()
    cant = len(laws)
    for law in laws:
        partys = []
        question = Question.objects.filter(law=law)
        votes = Voting.objects.filter(law=law)
        choice = Choice.objects.filter(user=user, question=question)
        if len(choice) > 0:
            choice = choice[0]
            for vote in votes:
                counts[vote.person] += 0
                if choice.choice.vote != 'INDIFERENTE' and choice.choice == vote.vote:
                    counts[vote.person] += 1
    results_by_person = []
    for x in counts:
        results_by_person.append((x.key, counts[x]/cant * 100.0))

    context = {'results_by_person': results_by_person}
    return render(request, 'webapp/results.html', context)


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
    expedients = set()
    for eo in doc.get_entity_occurrences():
        e = eo.entity
        if e.kind.name == 'LAW':
            law = e.key
        elif e.kind.name == 'EXPEDIENT':
            expedients.add(e.key)
    context = {'doc': doc, 'expedients': expedients, 'law': law, 'evidences': res}
    return render(request, 'webapp/evidences.html', context)


def load_laws(request):
    if not request.user.is_authenticated():
        return HttpResponse('Necesitas estar loggeado.')

    docs = IEDocument.objects.all()
    for doc in docs:
        evidences = EvidenceCandidate.objects.all()
        # entity_ocurrences = doc.get_entity_occurrences
        segments_id = [x.id for x in doc.get_text_segments()]

        # Collect data from iepy models
        law = None
        expedient = None
        for eo in doc.get_entity_occurrences():
            e = eo.entity
            if law is None and e.kind.name == 'LAW':
                #law = e.key
                law = e
            elif expedient is None and e.kind.name == 'EXPEDIENT':
                expedient = e.key
                #expedient = e
        assert law is not None and expedient is not None

        # Save Law model
        l = Law()
        l.expedient = expedient
        l.law = law
        l.status = True
        l.save()
        ok = True

        # Save Question model
        #if ok and len(Question.objects.filter(law=l)) == 0:
        if ok:
            q = Question()
            q.law = l
            q.question = law.key #Falta hacer
            q.save()
            ok = True

        # Create votes
        if len(Vote.objects.filter(vote='AFIRMATIVO')) == 0:
            vo = Vote()
            vo.vote = 'AFIRMATIVO'
            vo.save()
        if len(Vote.objects.filter(vote='NEGATIVO')) == 0:
            vo = Vote()
            vo.vote = 'NEGATIVO'
            vo.save()
        if len(Vote.objects.filter(vote='INDIFERENTE')) == 0:
            vo = Vote()
            vo.vote = 'INDIFERENTE'
            vo.save()

        # Collect more data from iepy models
        for evidence in evidences:
            first_label = evidence.labels.first()
            if evidence.segment_id in segments_id and first_label.label == 'YE':
                    person = evidence.left_entity_occurrence.entity
                    if evidence.right_entity_occurrence.alias == 'AFIRMATIVO':
                        vote = Vote.objects.filter(vote='AFIRMATIVO')[0]
                    elif evidence.right_entity_occurrence.alias == 'NEGATIVO':
                        vote = Vote.objects.filter(vote='NEGATIVO')[0]
                    else:
                        vote = Vote.objects.filter(vote='INDIFERENTE')[0]

                    # Save Voting model
                    if ok and len(Voting.objects.filter(person=person, law=l)) == 0:
                        v = Voting()
                        v.law = l
                        v.person = person
                        v.vote = vote
                        v.save()

    return HttpResponse('Done!')
