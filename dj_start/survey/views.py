from math import ceil
import logging

from django.shortcuts import (render, HttpResponseRedirect,
                              Http404, get_object_or_404, HttpResponse)
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from survey.models import Survey, Question, Answer, Page, Result
from closealternative import Finder

logger = logging.getLogger(__name__)


def get_pages(num_elements, limit):
    pages = []
    num_pages = int(ceil(float(num_elements) / limit))

    for i in xrange(1, num_pages+1):
        pages.append(i)
    return pages


class ListView(View):
    template_name = 'survey/list.html'

    def get(self, request, page=1, limit=3):
        page = int(page)
        limit = int(limit)
        offset = (page - 1) * limit
        surveys = Survey.get_objects(limit, offset)

        if not surveys:
            raise Http404

        num_surveys = Survey.get_num_surveys()
        count_start = offset + 1
        pages = get_pages(num_surveys, limit)
        context = {
            'surveys': surveys,
            'current_page': page,
            'count_start': count_start,
            'pages': pages,
            'limit': limit
        }

        return render(request, self.template_name, context)


class SurveyView(View):
    template_name = 'survey/survey.html'
    SURVEY_PAGE = 'survey_page'

    def get(self, request, survey_id, page=1):
        survey = get_object_or_404(Survey, pk=survey_id)
        page = int(page)
        next_page = Page.get_next_page(survey_id, page)
        session_page = request.session.get(self.SURVEY_PAGE, 1)
        if page != session_page:
            #return HttpResponseRedirect(reverse('survey:survey', args=(survey_id, session_page)))
            pass
        if page == 1:
            request.session['answers'] = []

        questions = Question.objects.filter(page__page_num=page, page__survey=survey_id)

        context = {
            'survey': survey,
            'questions': questions,
            'next_page': next_page,
            'current_page': page
        }
        return render(request, self.template_name, context)

    def post(self, request, survey_id, page=1):
        questions_on_page = Question.objects.filter(page__page_num=page, page__survey=survey_id)
        survey = get_object_or_404(Survey, pk=survey_id)
        unanswered_q = []
        answered = []
        answers_so_far = request.session.get('answers', [])
        for q in questions_on_page:
            answer_ids_str = request.POST.getlist('question[{}]'.format(q.id))
            try:
                answer_ids = map(int, answer_ids_str)
            except ValueError as e:
                answer_ids = []
                unanswered_q.append(q.id)
                logger.info(e)

            if answer_ids:
                answers_so_far += answer_ids
                answered += answer_ids
            else:
                unanswered_q.append(q.id)
        next_page = Page.get_next_page(survey_id, page)

        if len(unanswered_q) == 0:
            request.session['answers'] = answers_so_far
            if next_page:
                # there is another page
                request.session[SurveyView.SURVEY_PAGE] = next_page
                return HttpResponseRedirect(reverse('survey:survey', args=(survey_id, next_page)))

            else:
                # finished the survey
                return HttpResponseRedirect(reverse('survey:result', args=(survey_id,)))
        # some questions were not answered
        questions = Question.objects.filter(page__page_num=page, page__survey=survey_id)
        context = {
            'unanswered': unanswered_q,
            'answered': answered,
            'survey': survey,
            'next_page': next_page,
            'questions': questions,
            'current_page': page
        }
        return render(request, self.template_name, context)


class ResultView(View):
    template_name = 'survey/result.html'

    def get(self, request, survey_id):
        answer_ids = request.session.get('answers', [])
        score = Answer.get_score_sum(survey_id, answer_ids)
        request.session['score'] = score

        result = Result.get_result(survey_id, score)
        context = {
            'result': result,
            'score': score,
            'survey_id': survey_id
        }
        logging.debug('score: {}'.format(score))
        return render(request, self.template_name, context)


class ClosestPath(View):
    def get(self, request, survey_id):
        try:
            score = int(request.session.get('score', None))
        except TypeError:
            return HttpResponse("no score")
        next_result = Result.get_result_above(survey_id, score)
        prev_result = Result.get_result_below(survey_id, score)
        given_ans = request.session.get('answers')

        pages = Page.objects.filter(survey=survey_id)
        data = {}
        points = {}
        for page in pages:
            answers = Answer.objects.filter(question__page=page)
            data[page.id] = {}
            for ans in answers:
                data[page.id][ans.question.id] = data[page.id].get(ans.question, [])
                data[page.id][ans.question.id].append(ans.id)
                points[ans.id] = ans.score


        f = Finder(current_score=score,
                   next_result=next_result,
                   previous_result=prev_result,
                   answers=given_ans,
                   pages=data,
                   points=points)
        f.compute()
        return HttpResponse("my very awesome response")
