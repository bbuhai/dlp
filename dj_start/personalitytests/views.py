import logging

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import Sum

from personalitytests.models import Test, Question, Answer, Score


logger = logging.getLogger(__name__)


class HomeView(generic.ListView):
    template_name = 'personalitytests/tests_list.html'
    context_object_name = 'tests'
    model = Test

    def get_queryset(self):
        logger.debug('listing tests...')
        return Test.objects.order_by('-created_at').all()


def test(request, test_id):
    pers_test = get_object_or_404(Test, pk=test_id)
    questions = pers_test.question_set.all()
    ans = []
    unanswered_q = []

    if request.method == 'POST':
        question_ids = (q.id for q in questions)

        for q_id in question_ids:
            try:
                ans.append(int(request.POST['answers[{}]'.format(q_id)]))
            except KeyError:
                unanswered_q.append(q_id)
            except ValueError as e:
                unanswered_q.append(q_id)
                logger.info(e)

        if len(unanswered_q) == 0:
            score = Answer.objects.filter(id__in=ans).aggregate(Sum('points'))
            score = score['points__sum'] or 0
            return HttpResponseRedirect(reverse('pers:result', args=(test_id, score)))

    context = {
        'test': pers_test,
        'questions': questions,
        'given_ans': ans,
        'unanswered_q': unanswered_q
    }
    return render(request, 'personalitytests/taketest.html', context)


def result(request, test_id, score):
    pers_test = get_object_or_404(Test, pk=test_id)
    try:
        user_result = Score.objects.filter(
            min_score__lte=score,
            max_score__gte=score,
            test=test_id
        ).all()[0]
    except IndexError:
        raise Http404
    context = {'result': user_result, 'test': pers_test}
    return render(request, 'personalitytests/result.html', context)