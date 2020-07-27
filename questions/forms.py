from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple

from .models import Question, Choice, ChoiceGroup


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'choice_group', 'choice', 'notes',)

        widgets = {
            # 'choice': forms.RadioSelect(attrs={'style': 'display: inline-block' }),
            'notes': forms.TextInput,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['choice_group'].queryset = ChoiceGroup.objects.filter(created_by=user)
        self.fields['choice'].queryset = Choice.objects.none()

        if 'choice_group' in self.data:
            try:
                choice_group_id = int(self.data.get('choice_group'))
                self.fields['choice'].queryset = Choice.objects.filter(choice_group_id=choice_group_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Choice queryset
        elif self.instance.pk:
            self.fields['choice'].queryset = self.instance.choice_group.choice_set


class QuestionAdminForm(forms.ModelForm):
    # choice = forms.MultipleChoiceField(
    #     required=False,
    #     label='Subject',
    #     widget=CheckboxSelectMultiple(),
    #     choices=Subject.objects.all()
    # )

    class Meta:
        model = Question
        fields = ('question_text', 'choice_group', 'choice', 'review_status', 'tags', 'notes',)

        widgets = {
            # 'choice': forms.RadioSelect(attrs={'style': 'display: inline-block' }),
            'notes': forms.TextInput,
            # 'feedback': forms.TextInput,
            # 'subject' : forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple()),
            # 'created_by': forms.TextInput,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['choice_group'].queryset = ChoiceGroup.objects.all()
        self.fields['choice'].queryset = Choice.objects.none()

        if 'choice_group' in self.data:
            try:
                choice_group_id = int(self.data.get('choice_group'))
                self.fields['choice'].queryset = Choice.objects.filter(choice_group_id=choice_group_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Choice queryset
        elif self.instance.pk:
            self.fields['choice'].queryset = self.instance.choice_group.choice_set



class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice', 'choice_group',)

    widgets = {
        # 'choice': forms.RadioSelect(attrs={'style': 'display: inline-block' }),
        'choice': forms.TextInput,
    }

