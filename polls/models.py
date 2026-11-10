import datetime
from django.contrib import admin
from django.db import models
from django.db.models import Max
from django.utils import timezone



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def age(self):
        return timezone.now() - self.pub_date

    def get_choice(self):
        choices = []
        total_votes = sum(choice.votes for choice in self.choice_set.all())
        for choice in self.choice_set.all():
            choices.append((choice.choice_text, choice.id, ((choice.votes/total_votes)*100 if total_votes > 0 else 0)))
        return choices

    def get_max_choice(self):
        return self.choice_set.all().aggregate(Max('votes'))['votes__max']

    def __str__(self):
        return (f"{self.question_text[:20]} publié le {self.pub_date}")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text[:20]
