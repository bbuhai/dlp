"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, SimpleTestCase
from closealternative import AnsTuple, DiscoverPath
from models import Result


def get_answers():
    return {
        1: {
            1: [AnsTuple(id=1, score=-5), AnsTuple(id=2, score=5)],
            2: [AnsTuple(id=9, score=1)],
            5: [AnsTuple(id=13, score=-3), AnsTuple(id=14, score=10)]
        },
        2: {
            3: [AnsTuple(id=10, score=-2)],
            4: [AnsTuple(id=16, score=2)]
        }
    }


def get_other_answers():
    return {
        1: {
            1: [AnsTuple(id=5, score=10)],
            2: [AnsTuple(id=8, score=0), AnsTuple(id=15, score=2)],
            5: []
        },
        2: {
            3: [AnsTuple(id=11, score=0)],
            4: [AnsTuple(id=12, score=1), AnsTuple(id=17, score=3)]
        }
    }


def get_score():
    return 8


def get_prev_result():
    return Result(min_score=-9, max_score=0, id=1, summary='Low end')


def get_next_result():
    return Result(min_score=15, max_score=35, id=3, summary='Top top!')


class DiscoverPathTest(SimpleTestCase):

    def test_final_for_better(self):
        next_result = get_next_result()
        prev_result = get_prev_result()
        disc = DiscoverPath(score=get_score(), next_result=next_result, prev_result=prev_result,
                            answers=get_answers(), other_answers=get_other_answers())
        result = disc._get_changes(next_result.min_score - get_score())

        self.assertEqual(len(result), 1)
        self.assertTrue(1 in result)
        self.assertEqual(result[1].val, 1)
        self.assertEqual(result[1].rm, [])
        self.assertEqual(result[1].add[0], AnsTuple(id=5, score=10))
        self.assertEqual(result[1].q, 1)
        self.assertEqual(result[1].pg, 1)
        self.assertEqual(result[1].score, 10)

    def test_final_for_worse(self):
        self.assertEqual(1, 1)

    def test_weight_higher_better(self):
        disc = DiscoverPath(score=get_score(), next_result=get_next_result(), prev_result=get_prev_result(),
                            answers=get_answers(), other_answers=get_other_answers())
        weights = disc.weight_questions()
        self.assertEqual(len(weights), 2)

        self.assertEqual(weights[1][1].val, 1)
        self.assertEqual(weights[1][1].pg, 1)
        self.assertEqual(weights[1][1].score, 10)
        self.assertEqual(weights[1][1].rm, [])
        self.assertEqual(len(weights[1][1].add), 1)

        self.assertEqual(weights[1][2].val, 1)
        self.assertEqual(weights[1][2].pg, 2)
        self.assertEqual(weights[1][2].score, 3)
        self.assertEqual(weights[1][2].rm, [])
        self.assertEqual(len(weights[1][2].add), 1)

        self.assertEqual(weights[2][1].val, 2)
        self.assertEqual(weights[2][1].pg, 1)
        self.assertEqual(weights[2][1].score, 15)
        self.assertEqual(len(weights[2][1].rm), 1)
        self.assertEqual(len(weights[2][1].add), 1)

        self.assertEqual(weights[2][2].val, 2)
        self.assertEqual(weights[2][2].pg, 2)
        self.assertEqual(weights[2][2].score, 4)
        self.assertEqual(weights[2][2].rm, [])
        self.assertEqual(len(weights[2][2].add), 2)

    def test_weight_lower_better(self):
        disc = DiscoverPath(score=get_score(), next_result=get_next_result(), prev_result=get_prev_result(),
                            answers=get_answers(), other_answers=get_other_answers())
        disc.higher_is_better = False
        weights = disc.weight_questions()
        self.assertEqual(len(weights), 2, 'Not enough weights.')

        self.assertEqual(len(weights[1]), 1, 'Only page one can have improvements with weight=1')
        self.assertEqual(weights[1][1].val, 1)
        self.assertEqual(weights[1][1].score, -10)
        self.assertEqual(len(weights[1][1].rm), 1)
        self.assertEqual(weights[1][1].add, [])

        self.assertEqual(len(weights[2]), 1, 'Only page two can have improvements with weight=2')
        self.assertEqual(weights[2][2].val, 2)
        self.assertEqual(weights[2][2].score, -1)
        self.assertEqual(len(weights[2][2].rm), 1)
        self.assertEqual(len(weights[2][2].add), 1)
