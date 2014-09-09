import heapq
import logging
from operator import attrgetter
from collections import namedtuple
import copy


logger = logging.getLogger(__name__)

AnsTuple = namedtuple("AnsTuple", ['id', 'score'])
Weight = namedtuple('Weight', ['val', 'rm', 'add', 'q', 'pg', 'score'])


def _extract_worst(n, lst):
    """Try to remove the smallest elements from a list and
    return them if the sum of the remaining is bigger than before.
    >>> lst = [AnsTuple(1, -10), AnsTuple(2, 0), AnsTuple(3, 10), AnsTuple(4, -1)]
    >>> _extract_worst(3, lst)
    [AnsTuple(id=1, score=-10), AnsTuple(id=4, score=-1), AnsTuple(id=2, score=0)]
    >>> lst = [AnsTuple(1, 10), AnsTuple(2, 1), AnsTuple(3, 10), AnsTuple(4, -1)]
    >>> _extract_worst(0, lst)
    []
    """
    if n < 1:
        return []
    return heapq.nsmallest(n, lst, key=attrgetter('score'))


def _extract_best(n, lst):
    """Try to remove the largest elements from a list and
    return them if the sum of the remaining is smaller than before.
    >>> lst = [AnsTuple(1, -10), AnsTuple(2, 0), AnsTuple(3, -20), AnsTuple(4, -1)]
    >>> _extract_best(2, lst)
    [AnsTuple(id=2, score=0), AnsTuple(id=4, score=-1)]
    >>> lst = [AnsTuple(1, 10), AnsTuple(2, 1), AnsTuple(3, 15), AnsTuple(4, -1)]
    >>> _extract_best(0, lst)
    []
    """
    if n < 1:
        return []
    return heapq.nlargest(n, lst, key=attrgetter('score'))


class DiscoverPath(object):
    def __init__(self, score, next_result, prev_result, answers, other_answers):
        self.score = score
        self.next = next_result
        self.prev = prev_result
        self.answers = answers
        self.other_answers = other_answers
        self.routes = []
        self.higher_is_better = True
        if next_result:
            self.routes.append(1)
        if prev_result:
            self.routes.append(-1)
        if not self.routes:
            raise ValueError('No possible path. Next and previous possible results are missing.')

    def compute(self):
        results = {}
        for route in self.routes:
            if route == 1:
                points_needed = self.next.min_score - self.score
                results['better'] = self._get_changes(points_needed)

            else:
                self.higher_is_better = False
                # + 1 because the interval is [min_score, max_score)
                points_needed = self.score - self.prev.max_score + 1
                results['worse'] = self._get_changes(points_needed)

        return results

    def _get_changes(self, points_needed):
        all_possible_changes = []
        w_q = self.weight_questions()
        sorted_weights = {}
        for w, details in w_q.iteritems():
            sorted_weights[w] = sorted(details.itervalues(), key=attrgetter('score'), reverse=self.higher_is_better)

        for w, details in sorted_weights.iteritems():
            i = 0
            length = len(details)
            points_needed_cpy = points_needed
            changes = {}
            while points_needed_cpy > 0 and i < length:
                page = details[i].pg
                if self.higher_is_better:
                    points_needed_cpy -= details[i].score
                else:
                    points_needed_cpy += details[i].score

                changes[page] = details[i]
                i += 1
                if points_needed_cpy <= 0:
                    continue
                for prev_weight in range(1, w):
                    prev_details = sorted_weights[prev_weight]
                    prev_length = len(prev_details)
                    points = points_needed_cpy
                    j = 0
                    inner_changes = {}
                    while points > 0 and j < prev_length:
                        obj = prev_details[j]
                        j += 1
                        if obj.pg in changes:
                            continue
                        inner_changes[obj.pg] = obj
                        if self.higher_is_better:
                            points -= obj.score
                        else:
                            points += obj.score

                    if points <= 0:
                        changes_copy = copy.copy(changes)
                        changes_copy.update(inner_changes)
                        all_possible_changes.append(changes_copy)

            if points_needed_cpy <= 0:
                all_possible_changes.append(changes)
        best = self._chose_best(all_possible_changes)
        return best

    @staticmethod
    def _chose_best(all_changes):
        best = None
        bestW = None
        for changes in all_changes:
            s = sum(w.val for w in changes.itervalues())
            if best is None or s < best:
                best = s
                bestW = changes
        return bestW

    def weight_questions(self):
        w = {}

        for page_id, questions in self.answers.iteritems():
            for q_id, ans in questions.iteritems():
                num_ans = len(ans) + len(self.other_answers[page_id][q_id])
                for weight in range(1, num_ans + 1):
                    best_weight = self._get_best_on_page_for_weight(
                        weight=weight,
                        page_id=page_id,
                        q_id=q_id,
                        all_weights=w
                    )

                    if best_weight:
                        w[weight] = w.get(weight, {})
                        if not page_id in w[weight]:
                            w[weight][page_id] = best_weight
                            continue
                        prev_weight = w[weight][page_id]
                        if prev_weight.score < best_weight.score and self.higher_is_better\
                                or prev_weight.score > best_weight.score and not self.higher_is_better:
                            w[weight][page_id] = best_weight

        return w

    def _get_best_on_page_for_weight(self, weight, page_id, q_id, all_weights):
        best_weight = None
        for j in range(0, weight+1):
            if self.higher_is_better:
                smallest = _extract_worst(j, self.answers[page_id][q_id])
                largest = _extract_best(abs(weight-j), self.other_answers[page_id][q_id])
            else:
                smallest = _extract_best(j, self.answers[page_id][q_id])
                largest = _extract_worst(abs(weight-j), self.other_answers[page_id][q_id])
            if not smallest and not largest:
                # no changes
                continue
            if len(smallest) + len(largest) != weight:
                continue
            new_set = self._combine_answers(self.answers[page_id][q_id], smallest, largest)

            if not new_set:
                # the question should have an answer
                continue
            score_improvement = sum(a.score for a in new_set) - \
                                sum(a.score for a in self.answers[page_id][q_id])

            if not self._is_improvement_bigger(
                    score_improvement, weight, page_id, all_weights
            ) or score_improvement == 0:
                continue
            # if improvement less equal that other weights less that this one => skip
            if best_weight is None or score_improvement > best_weight.score and self.higher_is_better\
                    or score_improvement < best_weight.score and not self.higher_is_better:
                best_weight = Weight(
                    val=weight,
                    score=score_improvement,
                    rm=smallest,
                    add=largest,
                    q=q_id,
                    pg=page_id)
        return best_weight

    def _is_improvement_bigger(self, score_improvement, weight_val, page_id, all_weights):
        if self.higher_is_better and score_improvement < 0:
            return False
        if not self.higher_is_better and score_improvement > 0:
            return False
        try:
            prev_weight_improvement = all_weights[weight_val-1][page_id]
        except KeyError:
            return True
        if prev_weight_improvement.score >= score_improvement and self.higher_is_better\
                or prev_weight_improvement.score <= score_improvement and not self.higher_is_better:
            return False
        return True

    @staticmethod
    def _combine_answers(initial, to_remove, to_add):
        answers = [a for a in initial if a not in to_remove]
        return answers + to_add

def _main():
    import doctest
    doctest.testmod()
if __name__ == '__main__':
    _main()