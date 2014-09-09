from collections import namedtuple
from operator import attrgetter
import heapq


AnsTuple = namedtuple("Ans", ['id', 'score'])
QTuple = namedtuple('Question', ['id', 'a', 'type'])
Weight = namedtuple('Weight', ['val', 'rm', 'add', 'q', 'pg', 'score'])
points = []


def _extract_worst(n, lst):
    """Try to remove the smallest elements from a list and
    return them if the sum of the remaining is bigger than before.
    >>> lst = [AnsTuple(1, -10), AnsTuple(2, 0), AnsTuple(3, 10), AnsTuple(4, -1)]
    >>> _extract_worst(3, lst)
    [Ans(id=1, score=-10), Ans(id=4, score=-1), Ans(id=2, score=0)]
    >>> lst = [AnsTuple(1, 10), AnsTuple(2, 1), AnsTuple(3, 10), AnsTuple(4, -1)]
    >>> _extract_worst(2, lst)
    []
    """
    s_all = sum(i.score for i in lst)
    smallest = heapq.nsmallest(n, lst, key=attrgetter('score'))
    s_small = sum(i.score for i in smallest)
    if s_all < s_all - s_small:
        return smallest
    return []


def _extract_best(n, lst):
    """Try to remove the largest elements from a list and
    return them if the sum of the remaining is smaller than before.
    >>> lst = [AnsTuple(1, -10), AnsTuple(2, 0), AnsTuple(3, -20), AnsTuple(4, -1)]
    >>> _extract_best(2, lst)
    []
    >>> lst = [AnsTuple(1, 10), AnsTuple(2, 1), AnsTuple(3, 15), AnsTuple(4, -1)]
    >>> _extract_best(2, lst)
    [Ans(id=3, score=15), Ans(id=1, score=10)]
    """
    s_all = sum(i.score for i in lst)
    largest = heapq.nlargest(n, lst, key=attrgetter('score'))
    s_big = sum(i.score for i in largest)
    if s_all > s_all - s_big:
        return largest
    return []


def compute_weights():
    ans_given = [AnsTuple(id=1, score=-2), AnsTuple(id=3, score=-8)]
    ans_given_per_q = ans_given
    points = []
    weights = {}
    pages = {
        'p1': {
            'q1': [AnsTuple(id=1, score=-2), AnsTuple(id=2, score=12), AnsTuple(id=3, score=-8)]
        }
    }
    p = {}
    for page, qs in pages.iteritems():
        p[page] = {}
        for q, anss in qs.iteritems():
            num_ans = len(anss)
            other_ans = [a for a in anss if a not in ans_given]
            for i in range(1, num_ans+1):
                best_crt_weight = None
                for j in range(0, i+1):
                    wst = _extract_worst(j, ans_given)
                    bst = _extract_best(i-j, other_ans)
                    if not wst and not bst:
                        # no changes
                        continue
                    # from ans_given_per_q
                    # remove worst answers
                    # and add best answers
                    # then if that combination is empty => skip to next (continue)
                    score = sum(ans_given - wst + bst)
                    if best_crt_weight is None or score > best_crt_weight.score:
                        best_crt_weight = Weight(val=i, rm=wst, add=bst, q=q, pg=page, score=score)
                weights[i] = best_crt_weight
"""
Notes:
- pass answers_given like this:
    {
        question_id1: [Ans1, Ans2, Ans3, Ans4],
        question_id2: [Ans5, Ans6, Ans7, Ans8]
    }
- pass answers_per_question in a similar fashion (send directly only the other answers maybe):
    {
        page_num: {
            question_id1: [Ans1, Ans2, Ans3, Ans4, Ans0],
            question_id2: [Ans5, Ans6, Ans7, Ans8, Ans9]
        }
    }
-  final weights:
    {
        1: {
            page_num: Weight(val=i, rm=wst, add=bst, q=q, pg=page, score=score),
            page_num: Weight(val=i, rm=wst, add=bst, q=q, pg=page, score=score),
        }
        2: {
            page_num: Weight(val=i, rm=wst, add=bst, q=q, pg=page, score=score),
            page_num: Weight(val=i, rm=wst, add=bst, q=q, pg=page, score=score),
        }
    }
- traverse weights from lowers to highest and then from highest score to lowest until points needed <= 0
- also combination of weights will be necessary (w1 from page 1 and w2 from page 2)
    => use nlargest and nsmallest there also
- do the same in reverse (for a lower score category)
"""

def main():
    import doctest
    doctest.testmod()
if __name__ == '__main__':
    main()