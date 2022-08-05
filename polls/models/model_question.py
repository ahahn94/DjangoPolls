import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        today = timezone.now()
        yesterday = today - datetime.timedelta(days=1)
        return yesterday <= self.pub_date <= today

    def __str__(self):
        return self.question_text
