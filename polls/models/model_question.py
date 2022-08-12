import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description="Published recently?"
    )
    def was_published_recently(self):
        today = timezone.now()
        yesterday = today - datetime.timedelta(days=1)
        return yesterday <= self.pub_date <= today

    def __str__(self):
        return self.question_text
