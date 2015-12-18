from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from iepy.data.models import *
from voting.webapp.models import *
from collections import defaultdict
import random


# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        title = 'Acceso ilegal'
        msg = 'Debes iniciar sesion para poder ver esta página.'
        context = {'title': title, 'msg': msg}
        return render(request, 'webapp/message.html', context)

    context = {'section': 'home'}
    return render(request, 'webapp/index.html', context)


def question(request):
    if not request.user.is_authenticated():
        title = 'Acceso ilegal'
        msg = 'Debes iniciar sesion para poder ver esta página.'
        context = {'title': title, 'msg': msg}
        return render(request, 'webapp/message.html', context)

    # generar la pregunta y llamar a save_choice
    user = User.objects.get(id=request.user.id)
    choices = Choice.objects.filter(user=user)
    questions_ans = [x.question for x in choices]
    questions = [x for x in Question.objects.all() if x not in questions_ans]
    if len(questions) <= 0:
        title = 'Respondiste a todas las preguntas'
        msg = 'Quieres ver los resultados?'
        links = [('Resultados', '/webapp/results')]
        context = {'title': title, 'msg': msg, 'links': links, 'section': 'question'}
        return render(request, 'webapp/message.html', context)

    selected = random.choice(questions)

    context = {'question': selected, 'section': 'question'}
    return render(request, 'webapp/question.html', context)


def save_choice(request):
    if not request.user.is_authenticated():
        title = 'Acceso ilegal'
        msg = 'Debes iniciar sesion para poder ver esta página.'
        return render(request, 'webapp/message.html', {'title': title, 'msg': msg})

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

        if len(Choice.objects.filter(user=user, question=question)) == 0:
            ch = Choice()
            ch.user = user
            ch.question = question
            ch.choice = vote
            ch.save()
        #return redirect('/webapp/question')
        title = 'Guardada exitosamente!'
        msg = 'Quieres responder otra pregunta para que los resultados sean mas precisos?'
        links = [('Responder otra pregunta', '/webapp/question')]
        links.append(('Ver los resultados parciales', '/webapp/results'))
        context = {'title': title, 'msg': msg, 'links': links, 'section': 'question'}
        return render(request, 'webapp/message.html', context)

    title = 'Acceso ilegal'
    msg = 'No tienes permiso para ver esta página.'
    return render(request, 'webapp/message.html', {'title': title, 'msg': msg})


def results(request):
    if not request.user.is_authenticated():
        title = 'Acceso ilegal'
        msg = 'Debes iniciar sesion para poder ver esta página.'
        return render(request, 'webapp/message.html', {'title': title, 'msg': msg})
    counts = defaultdict(int)
    counts_party = defaultdict(int)
    person_party = {}
    user = User.objects.get(id=request.user.id)
    docs = IEDocument.objects.all()
    cant_laws = 0
    for doc in docs:
        evidences = EvidenceCandidate.objects.all()
        segments_id = [x.id for x in doc.get_text_segments()]
        # Collect data from iepy models
        laws = []
        # Falta usar los expedientes
        expedients = []
        for eo in doc.get_entity_occurrences():
            e = eo.entity
            if e.kind.name == 'LAW':
                laws.append(e)
            elif e.kind.name == 'EXPEDIENT':
                expedients.append(e)
        if len(laws) == 0:
            continue
        cant_laws += len(laws)


        for evidence in evidences:
            """first_label = evidence.labels.first()
            if first_label is None:
                continue"""
            first_label = Label.objects.filter(evidence=evidence)
            if len(first_label) == 0:
                continue
            first_label = first_label[0]
            #if evidence.segment_id in segments_id and first_label.label == 'YE':
            if evidence.segment_id in segments_id and first_label.label == True:
                for law in laws:
                    # Falta implementar para muchas preguntas de la misma ley
                    question = Question.objects.filter(law=law)
                    choice = Choice.objects.filter(user=user, question=question)
                    if len(choice) > 0:
                        choice = choice[0]
                        leo = evidence.left_entity_occurrence
                        reo = evidence.right_entity_occurrence
                        if first_label.relation.name == 'person_vote':
                            if reo.alias != 'AFIRMATIVO' and reo.alias != 'NEGATIVO':
                                vote = Vote.objects.get(vote='INDIFERENTE')
                            else:
                                vote = Vote.objects.get(vote=reo.alias)
                            counts[leo.alias] += 0
                            if choice.choice.vote != 'INDIFERENTE' and choice.choice == vote:
                                counts[leo.alias] += 1
                        elif first_label.relation.name == 'person_party':
                            person_party[leo.alias] = reo.alias
                    else:
                        print('El usuario no respondio ninguna pregunta.')
    results_by_person = []
    results_by_party = []
    for person in counts:
        val = counts[person]/cant_laws * 100.0
        #results_by_person.append((person, val))
        #results_by_person.append((round(val, 2), person))
        person_with_party = person + ' (' + person_party[person] + ')'
        results_by_person.append((round(val, 2), person_with_party))
        if person in person_party:
            party = person_party[person]
            counts_party[party] += counts[person]/cant_laws
    for party in counts_party:
        cant_persons = len([x for x in person_party if person_party[x] == party])
        val = counts_party[party]/cant_persons * 100.0
        rep_val = cant_persons / len(counts) * 100.0
        rep_index = (val + rep_val) / 2.0
        results_by_party.append((rep_index, round(val, 2), party, round(rep_val, 2)))
    results_by_person = sorted(results_by_person, reverse=True)
    results_by_party = sorted(results_by_party, reverse=True)
    if len(results_by_person) == 0:
        title = 'No se pueden mostrar los resultados'
        msg = 'Debes responder alguna pregunta antes.'
        return render(request, 'webapp/message.html', {'title': title, 'msg': msg})
    context = {'results_by_person': results_by_person, 'results_by_party': results_by_party, 'section': 'results'}
    return render(request, 'webapp/results.html', context)


def init(request):
    if not request.user.is_authenticated():
        title = 'Acceso ilegal'
        msg = 'Debes iniciar sesion para poder ver esta página.'
        return render(request, 'webapp/message.html', {'title': title, 'msg': msg})
    logs = []
    law_kind = EntityKind.objects.get(name='LAW')
    laws = Entity.objects.filter(kind=law_kind)
    for law in laws:
        if len(Question.objects.filter(law=law)) == 0:
            q = Question()
            q.law = law
            q.question = law.key #Falta hacer
            q.save()
            logs.append('Creacion de Pregunta: ' + law.key)

    # Create votes
    if len(Vote.objects.filter(vote='AFIRMATIVO')) == 0:
        vo = Vote()
        vo.vote = 'AFIRMATIVO'
        vo.save()
        logs.append('Creacion de Voto: ' + vo.vote)
    if len(Vote.objects.filter(vote='NEGATIVO')) == 0:
        vo = Vote()
        vo.vote = 'NEGATIVO'
        vo.save()
        logs.append('Creacion de Voto: ' + vo.vote)
    if len(Vote.objects.filter(vote='INDIFERENTE')) == 0:
        vo = Vote()
        vo.vote = 'INDIFERENTE'
        vo.save()
        logs.append('Creacion de Voto: ' + vo.vote)
    logs.append('Done!')

    return HttpResponse('<br /><br />'.join(logs))


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


"""def load_laws(request):
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
            #q.law = l
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
                        vote = Vote.objects.get(vote='AFIRMATIVO')
                    elif evidence.right_entity_occurrence.alias == 'NEGATIVO':
                        vote = Vote.objects.get(vote='NEGATIVO')
                    else:
                        vote = Vote.objects.get(vote='INDIFERENTE')

                    # Save Voting model
                    if ok and len(Voting.objects.filter(person=person, law=l)) == 0:
                        v = Voting()
                        v.law = l
                        v.person = person
                        v.vote = vote
                        v.save()

    return HttpResponse('Done!')"""

"""
results viejo
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
"""
