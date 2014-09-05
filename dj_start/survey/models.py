import datetime

from django.db import models


def get_first_value(qset):
    try:
        return qset[0]
    except IndexError:
        return None


class Survey(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
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

    @classmethod
    def get_objects(cls, limit, offset):
        end = offset + limit
        return cls.objects.all()[offset:end]

    @classmethod
    def get_num_surveys(cls):
        return cls.objects.count()

    class Meta:
        ordering = ['-created_at']


class Page(models.Model):
    page_num = models.PositiveIntegerField()
    survey = models.ForeignKey(Survey)

    def __unicode__(self):
        return "Pg {} from {}".format(self.page_num, self.survey)

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def get_next_page(cls, survey_id, page_num):
        query = cls.objects.filter(survey=survey_id, page_num__gt=page_num).order_by('page_num')
        try:
            page = query[0]
        except IndexError:
            return None
        return page.page_num

    class Meta:
        unique_together = ('page_num', 'survey')


class Question(models.Model):
    SINGLE = 'radio'
    MULTIPLE = 'checkbox'
    TYPE_IN_CHOICES = (
        (SINGLE, 'Single answer'),
        (MULTIPLE, 'Multiple answers')
    )

    page = models.ForeignKey(Page)
    question_text = models.CharField(max_length=300)
    position = models.IntegerField(help_text="Question order")
    type = models.CharField(max_length=20, choices=TYPE_IN_CHOICES, default=SINGLE)

    def __unicode__(self):
        return self.question_text[:10]

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['position']


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=200)
    score = models.IntegerField()

    def __unicode__(self):
        return self.answer_text[:10]

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def get_score_sum(cls, survey_id, answer_ids):
        q = cls.objects.filter(question__page__survey=survey_id,
                               id__in=answer_ids).aggregate(total=models.Sum('score'))
        return q['total']


class Result(models.Model):
    survey = models.ForeignKey(Survey)
    summary = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    min_score = models.IntegerField()
    max_score = models.IntegerField()

    def __unicode__(self):
        return self.summary[:10]

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def get_result(cls, survey_id, score):
        q = cls.objects.filter(survey=survey_id, max_score__gt=score, min_score__lte=score)
        return get_first_value(q)

    @classmethod
    def get_result_above(cls, survey_id, score):
        q = cls.objects.filter(survey=survey_id, min_score__gt=score).order_by('min_score')
        return get_first_value(q)

    @classmethod
    def get_result_below(cls, survey_id, score):
        q = cls.objects.filter(survey=survey_id, max_score__lt=score).order_by('-min_score')
        return get_first_value(q)


