from django.db import models


class Contact(models.Model):
    sender = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    cc_self = models.BooleanField()

    def __unicode__(self):
        return self.subject[:10]

    def __str__(self):
        self.__unicode__()
