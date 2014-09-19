from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Test(models.Model):
    name = models.CharField(max_length=200, verbose_name='Test name')
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def shorten_description(self, length=160):
        if len(self.description) > length - 3:  # 3 for the ellipses
            return self.description[:length] + '...'
        return self.description


class Question(models.Model):
    test = models.ForeignKey(Test)
    question = models.CharField(max_length=400)

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.__unicode__()


class Score(models.Model):
    test = models.ForeignKey(Test)
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    result = models.CharField(max_length=400)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.result[:20]


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=400)
    points = models.IntegerField()

    def __unicode__(self):
        return self.answer

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def get_total_points(cls, answer_ids):
        score = cls.objects.filter(id__in=answer_ids).aggregate(Sum('points'))
        return score['points__sum'] or 0


class UserScore(models.Model):
    user = models.ForeignKey(User)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now=True)