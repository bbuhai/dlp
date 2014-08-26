import datetime

from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=200, verbose_name='Test name')
    created_at = models.DateTimeField(default=datetime.datetime.now())
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test)
    question = models.CharField(max_length=400)


class Score(models.Model):
    test = models.ForeignKey(Test)
    min_score = models.IntegerField()
    max_score = models.IntegerField()
    result = models.CharField(max_length=400)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=400)
    points = models.IntegerField()
