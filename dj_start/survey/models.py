import datetime

from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    created_at = models.DateTimeField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        super(Survey, self).save(*args, **kwargs)

    def shorten_description(self, length=160):
        if len(self.description) > length - 3:  # 3 for the ellipses
            return self.description[:length] + '...'
        return self.description


class Page(models.Model):
    page_num = models.PositiveIntegerField()
    survey = models.ForeignKey(Survey)

    def __unicode__(self):
        return "Pg {} from {}".format(self.page_num, self.survey)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        unique_together = ('page_num', 'survey')


class Question(models.Model):
    page = models.ForeignKey(Page)
    question_text = models.CharField(max_length=300)
    position = models.IntegerField(help_text="Question order")

    def __unicode__(self):
        return self.question_text[:10]

    def __str__(self):
        return self.__unicode__()


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=200)
    score = models.IntegerField()

    def __unicode__(self):
        return self.answer_text[:10]

    def __str__(self):
        return self.__unicode__()


class Result(models.Model):
    survey = models.ForeignKey(Survey)
    summary = models.CharField(max_length=300)
    description = models.TextField(null=True)
    min_score = models.IntegerField()
    max_score = models.IntegerField()

    def __unicode__(self):
        return self.summary[:10]

    def __str__(self):
        return self.__unicode__()