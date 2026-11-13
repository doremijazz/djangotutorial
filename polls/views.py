import initial
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.db.models import F, Sum, Avg, Max, Model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import QuestionForm, ChoiceForm, ChoiceFormSet, PasswordForm
from .models import Choice, Question
from .forms import InscriptionForm

def connexion_personnalisee(request):
    erreur = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("polls:index")
        erreur = "Identifiants incorrects."
    return render(request, "polls/login.html", {"erreur": erreur})


def deconnexion(request):
    logout(request)
    return redirect("polls:index")

def register(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)

        if form.is_valid():
            utilisateur = form.save()
            return redirect("login")
    else:
        form = InscriptionForm()

    return render(
        request,
        "polls/register.html",
        {"form": form}
    )


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]
class UserView(generic.DetailView):
    model = User
    template_name = "polls/account.html"

class ChangePasswordView(PasswordChangeView):
    template_name = "polls/change_password.html"
    form_class = PasswordForm
    success_url = reverse_lazy("polls:account")


class AllView(generic.ListView):
    model = Question
    template_name = "polls/all.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


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
@login_required(login_url="polls:connexion_personnalisee")
def get_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        form_choices = ChoiceFormSet(request.POST)

        if form.is_valid() and form_choices.is_valid():
            choices = [
                choice_form.save(commit=False)
                for choice_form in form_choices
                if choice_form.cleaned_data
                and choice_form.cleaned_data.get("choice_text", "").strip()
            ]

            if not choices:
                form_choices._non_form_errors = form_choices.error_class(
                    ["Saisissez au moins une réponse."]
                )
            else:
                with transaction.atomic():
                    question = form.save(commit=False)
                    question.pub_date = timezone.now()
                    question.save()

                    for choice in choices:
                        choice.question = question
                        choice.votes = 0
                        choice.save()

                return redirect("polls:index")

    else:
        form = QuestionForm()
        form_choices = ChoiceFormSet()

    return render(
        request,
        "polls/form.html",
        {
            "form": form,
            "form_choices": form_choices,
        }
    )
@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
def change_question(request, pk):

    question = get_object_or_404(Question, pk=pk)
    choix = list(question.choice_set.all())

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        form_choices = ChoiceFormSet(request.POST)

        if form.is_valid() and form_choices.is_valid():

            nouvelles_reponses = [
                choice_form.cleaned_data["choice_text"].strip()
                for choice_form in form_choices
                if choice_form.cleaned_data
                and choice_form.cleaned_data.get("choice_text", "").strip()
                and not choice_form.cleaned_data.get("DELETE", False)
            ]

            if not nouvelles_reponses:
                form_choices._non_form_errors = form_choices.error_class(
                    ["Saisissez au moins une réponse."]
                )

            else:
                with transaction.atomic():

                    form.save()

                    for i, texte in enumerate(nouvelles_reponses):

                        if i < len(choix):
                            choice = choix[i]
                            choice.choice_text = texte
                            choice.save()
                        else:
                            Choice.objects.create(
                                question=question,
                                choice_text=texte,
                                votes=0
                            )

                    for choice in choix[len(nouvelles_reponses):]:
                        choice.delete()

                return redirect("polls:detail", pk=question.pk)

    else:
        form = QuestionForm(instance=question)

        form_choices = ChoiceFormSet(
            initial=[
                {"choice_text": choice.choice_text}
                for choice in choix
            ]
        )

    return render(
        request,
        "polls/change_question.html",
        {
            "form": form,
            "form_choices": form_choices,
            "question": question,
        }
    )



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