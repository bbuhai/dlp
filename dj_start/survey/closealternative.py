"""
current score
next result
previous result
answers

the potential of each question

"""
import heapq
import logging

logger = logging.getLogger(__name__)


class Finder(object):
    def __init__(self, current_score, next_result, previous_result, answers, pages, points):
        self.score = current_score
        self.next = next_result
        self.prev = previous_result
        self.answers = answers
        self.pages = pages
        self.routes = []
        self.points = points
        if next_result:
            self.routes.append(1)
        if previous_result:
            self.routes.append(-1)

    def compute(self):
        for route in self.routes:
            if route == 1:
                self.rate_questions_better()
            else:
                self.rate_question_worse()

    def rate_question_worse(self):
        points_needed = self.prev.max_score - self.score - 1
        rating = {}
        for page_id, questions in self.pages.iteritems():
            rating[page_id] = [0]
            for q_id, ans in questions.iteritems():
                # max
                s = sum(self.points[i] for i in ans
                        if i not in self.answers)
                rating[page_id].append((s, q_id, ))
            rating[page_id] = min(rating[page_id])

        rating = [j + (i,) for i, j in rating.iteritems()]
        rating.sort(reverse=True)

        idx = 0
        qs = []
        while idx < len(rating) and points_needed > 0:
            if isinstance(rating[idx], tuple):
                points_needed -= rating[idx][0]
                qs.append(rating[idx][1])
            idx += 1

        return rating

    def rate_questions_better(self):
        points_needed = self.next.min_score - self.score
        rating = {}
        for page_id, questions in self.pages.iteritems():
            rating[page_id] = [0]
            for q_id, ans in questions.iteritems():
                # max
                s = sum(self.points[i] for i in ans
                        if i not in self.answers and self.points[i] > 0)
                rating[page_id].append((s, q_id, ))
            rating[page_id] = max(rating[page_id])

        rating = [j + (i,) for i, j in rating.iteritems()]
        rating.sort(reverse=True)

        idx = 0
        qs = []
        while idx < len(rating) and points_needed > 0:
            if isinstance(rating[idx], tuple):
                points_needed -= rating[idx][0]
                qs.append(rating[idx][1])
            idx += 1

        return rating



    def check_higher(self):
        points_needed = self.next.min_score - self.score
        limits_per_page = []
        for page in self.pages:
            max_unans = 0
            min_ans = 0
            questions = self.pages[page]
            for q_id, ans_ids in questions.iteritems():
                not_ans = [(self.points[i], i) for i in ans_ids
                           if i not in self.answers]
                ans = [(self.points[i], i) for i in ans_ids
                       if i in self.answers]
                try:
                    max_points = max(not_ans)[0]
                except (KeyError, ValueError):
                    pass
                else:
                    if max_points > max_unans:
                        max_unans = max_points
                try:
                    min_points = min(ans)[0]
                except (KeyError, ValueError):
                    pass
                else:
                    if min_points < 0 and min_points < min_ans:
                        min_ans = min_points

            limits_per_page.append((max_unans, min_ans))
        extra = self.recc(points_needed, limits_per_page)
        return limits_per_page

    def recc(self, points_needed, per_page):
        idx = 0
        extra_points = []
        while points_needed > 0 and idx < len(per_page):
            if per_page[idx][0] > -per_page[idx][1]:
                points_needed -= per_page[idx][0]
                extra_points.append(per_page[idx][0])
            else:
                points_needed += per_page[idx][1]
                extra_points.append(per_page[idx][1])
            idx += 1

        return extra_points



    def check_lower(self):

        points_needed = self.score - self.prev.max_score
        for page in self.pages:
            questions = self.pages[page]
            for q_id, q_ans in questions.iteritems():
                pass


    def get_result(self):
        pass