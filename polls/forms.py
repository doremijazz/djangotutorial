from django.forms import ModelForm, Textarea, formset_factory
from .models import Question, Choice


class QuestionForm(ModelForm):
    template_name = "polls/form.html"

    class Meta:
        model = Question
        fields = ["question_text"]
        widgets = {
            "question_text": Textarea(attrs={"cols": 80, "rows": 5}),
        }
        help_texts = {
            "question_text": "Intitulé de la question"
        }

class ChoiceForm(ModelForm):
    template_name = "polls/form.html"

    class Meta:
        model = Choice
        fields = ["choice_text"]
        widgets = {
            "choice_text": Textarea(attrs={"cols": 80, "rows": 5}),
        }

ChoiceFormSet = formset_factory(
    ChoiceForm,
    extra=5,
    max_num=5,
    validate_max=True
)