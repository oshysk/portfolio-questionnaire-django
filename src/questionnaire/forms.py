from django import forms

from .models import Questionnaire, Choice, Answer


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ["title", "overview"]


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text"]

    def save(self, questionnaire_model: Questionnaire, commit=True):
        choice: Choice = super().save(commit=False)
        choice.questionnaire = questionnaire_model
        if commit:
            choice.save()
        return choice


class AnswerForm(forms.Form):

    def __init__(
        self,
        questionnaire_id: int,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.fields["choice"] = forms.ModelChoiceField(
            queryset=Choice.objects.filter(questionnaire_id=questionnaire_id),
            widget=forms.RadioSelect,
        )
        self.questionnaire_id = questionnaire_id

    def save(self, commit=True):
        answer: Answer = Answer(
            questionnaire_id=self.questionnaire_id,
            choice=self.cleaned_data["choice"],
        )
        if commit:
            answer.save()
        return answer
