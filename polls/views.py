from django.db.models import F, Sum, Avg, Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class AllView(generic.ListView):
    model = Question
    template_name = "polls/all.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object
        choices = question.choice_set.all()

        total_votes = sum(choice.votes for choice in choices)
        frequency = []
        for choice in choices:
            pourcentage = (choice.votes / total_votes * 100 if total_votes > 0 else 0)
            frequency.append({
            "text": choice.choice_text,
            "votes": choice.votes,
            "pourcentage": pourcentage}
            )

        context["frequency"] = frequency
        context["total_votes"] = total_votes

        return context
class StatisticsView(generic.TemplateView):
    model = Question
    template_name = "polls/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_questions"] = Question.objects.all().count()
        context["total_choices"] = Choice.objects.all().count()
        context["total_votes"] = Choice.objects.aggregate(total=Sum("votes"))["total"] or 0
        context["moyennes"] = [{"id" : q.id,
                               "moyenne" :  q.choice_set.aggregate(moyenne=Avg("votes"))["moyenne"] or 0}
                              for q in Question.objects.all()]
        context["last"] = Question.objects.order_by("-id").first()
        return context

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))