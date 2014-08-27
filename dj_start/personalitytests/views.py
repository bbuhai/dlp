from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from personalitytests.models import Test, Question, Answer


class HomeView(generic.ListView):
    template_name = 'personalitytests/home.html'
    context_object_name = 'tests'
    model = Test

    def get_queryset(self):
        return Test.objects.order_by('-created_at').all()


def test(request, test_id):
    pers_test = get_object_or_404(Test, pk=test_id)
    questions = pers_test.question_set.all()
    context = {'test': pers_test, 'questions': questions}
    return render(request, 'personalitytests/taketest.html', context)


def compute_score(request, test_id):
    if request.method == 'POST':
        questions = Question.objects.filter(test_id=test_id)
        #question_ids = [q.id for q in questions]
        #answers = questions.answers_set.all()
        #submitted = [request.POST['answers{}'.format(q.id)] for q in questions]
        


    return HttpResponseRedirect(reverse('pers:result', args=(test_id,)))


def result(request, test_id):
    return HttpResponse("Test result for id: {}".format(test_id))