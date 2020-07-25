from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from random import shuffle
from django.contrib import messages
import csv  #for csv
from django.http import HttpResponse #for csv
from django.core.paginator import Paginator

# from questions.models import Question, Choice, ChoiceGroup, Subject
from questions.forms import QuestionForm, ChoiceForm, QuestionAdminForm, QuestionSubjectForm
from questions.resources import *
from django.forms import inlineformset_factory
from django_filters.views import FilterView
from questions.filters import QuestionFilter


# Delete Questions, then Choices, then Groups
def index_view(request):
    return render(request, 'questions/index.html')


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    # fields = '__all__'
    success_url = reverse_lazy('questions:question-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class QuestionUpdateView(UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm

    # fields = ('question_text', 'choice_group', 'choice', 'notes',)
    success_url = reverse_lazy('questions:question-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        if self.request.user == self.get_object().created_by:
            return True
        else:
            return False


# Edit others questions
class QuestionAdminUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionAdminForm
    permission_required = ('can_access_subjects', 'can_edit_unreviewed_questions')

    # fields = ('question_text', 'choice_group', 'choice', 'notes',)
    success_url = reverse_lazy('questions:question-list-all')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # works if using UserPassesTestMixin
    # def test_func(self):
    #     if self.request.user.username == 'admin':  # Admin user id
    #         return True
    #     else:
    #         return False


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question

    def get_queryset(self):
        user = self.request.user
        question_list = Question.objects.order_by("-last_modified").filter(created_by=user).filter(
            review_status='UNREVIEWED')
        return question_list


class QuestionListAllView(LoginRequiredMixin, FilterView):
    model = Question
    template_name = "questions/question_filter.html"
    paginate_by = 5

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)

    # question_list = Question.objects.all()
    # paginator = Paginator(question_list, 5)

    def get_queryset(self):
        query_set = self.model.objects.all().order_by('created')
            # .order_by('last_modified')
        #.order_by('created_by', 'last_modified')
        question_filtered_list = QuestionFilter(self.request.GET, queryset=query_set)
        return question_filtered_list.qs


# Don't need it.  Working
# class QuestionListNextView(LoginRequiredMixin, ListView): #Supervisor Edits
#     model = Question
#     template_name = "questions/question_filter.html"
#
#     def get_queryset(self):
#         question_list = Question.objects.order_by("last_modified").filter(review_status='UNREVIEWED')[:5]
#         return question_list


# class QuestionDetailView(DetailView):
#     model = Question
#     # template_name = "questions/permission_required.html"
#     # permission_required = ('questions.can_view_all_questions')
#
#     def get_queryset(self):
#         # user = self.request.user
#         question_list = Question.objects.order_by("-last_modified").filter(review_status='UR')
#         return question_list
#
#     def get_context_data(self, **kwargs):
#         context = super(QuestionDetailView, self).get_context_data(**kwargs)
#         context['choices'] = Choice.objects.filter(self.model.choice_group)
#         # other code
#         return context

# class QuestionDetailView(LoginRequiredMixin, DetailView):
#     model = Question


# class QuestionDeleteView(LoginRequiredMixin, DeleteView):
#     model = Question
#     success_url = reverse_lazy('questions:question-list')
#
#     def get_queryset(self):
#         user = self.request.user
#         question_list = Question.objects.filter(created_by=user)
#         return question_list

def load_choices(request):
    choice_group_id = request.GET.get('choice_group')
    choices = Choice.objects.filter(choice_group_id=choice_group_id)
    return render(request, 'questions/choice_dropdown_list_options.html', {'choices': choices})


class QuestionSubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionSubjectForm
    permission_required = ('can_access_subjects', 'can_edit_unreviewed_questions')

    # fields = ('question_text', 'choice_group', 'choice', 'notes',)
    success_url = reverse_lazy('questions:question-list-all')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs




class ChoiceGroupCreateView(LoginRequiredMixin, CreateView):
    model = ChoiceGroup
    # form_class = ChoiceGroupForm
    fields = '__all__'
    # success_url = 'questions:index'
    success_url = reverse_lazy('questions:choice-group-create')

    # form = QuestionForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.username == "admin":
            context["objects"] = self.model.objects.all().order_by('last_modified')
        else:
            context["objects"] = self.model.objects.order_by('last_modified').filter(created_by=self.request.user)
        return context


class ChoiceGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ChoiceGroup
    fields = ('choice_group',)
    success_url = reverse_lazy('questions:choice-group-create')


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    # form_class = ChoiceGroupForm
    fields = '__all__'
    # success_url = 'questions:index'
    success_url = reverse_lazy('questions:subject-create')
    permission_required = ('can_access_subjects')

    # form = QuestionForm

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.username == "admin":
            context["objects"] = self.model.objects.all().order_by('subject')
        else:
            context["objects"] = self.model.objects.none()
        return context


class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    fields = ('subject',)
    success_url = reverse_lazy('questions:subject-create')
    permission_required = 'can_access_subjects'


# Works but don't need it
# class ChoiceGroupListView(LoginRequiredMixin, ListView):
#     model = ChoiceGroup
#     # permission_required = ('kidsapp.view_denial')
#     def get_queryset(self):
#         user = self.request.user
#         choice_group_list = ChoiceGroup.objects.filter(created_by=user)
#         return choice_group_list


# class ChoiceGroupDetailView(LoginRequiredMixin, DetailView):
#     model = ChoiceGroup


# class ChoiceGroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = ChoiceGroup
#     success_url = reverse_lazy('author-list')
#
#     def get_queryset(self):
#         user = self.request.user
#         choice_group_list = ChoiceGroup.objects.filter(created_by=user)
#         return choice_group_list


# class ChoiceCreateView(LoginRequiredMixin, CreateView):
#     model = Choice
#     # form_class = ChoiceGroupForm
#     fields = '__all__'
#     # success_url = 'questions:index'
#     success_url = reverse_lazy('questions:choice-list')
#
#     # form = QuestionForm
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

def choiceCreateView(request, pk):
    # form = ChoiceForm
    ChoiceFormSet = inlineformset_factory(ChoiceGroup, Choice, form=ChoiceForm, fields=('choice',), extra=5)
    choice_group = ChoiceGroup.objects.get(id=pk)

    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, instance=choice_group)
        if formset.is_valid():
            formset.save()
            return redirect('questions:choice-create', pk=choice_group.id)

    # IMPORTANT: Change queryset objects.none() to not show older items in list
    # formset = ChoiceFormSet(queryset=Choice.objects.none(),instance=choice_group)
    formset = ChoiceFormSet(queryset=Choice.objects.all(), instance=choice_group)
    context = {'formset': formset, 'choice_group': choice_group}
    return render(request, 'questions/choice_form.html', context)


class ChoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Choice
    fields = ('choice',)
    success_url = reverse_lazy('questions:choice-list')

    # def get_queryset(self):
    #     user = self.request.user
    #     choice_list = Choice.objects.filter(created_by=user)
    #     return choice_list


class ChoiceListView(LoginRequiredMixin, ListView):
    model = Choice


# class ChoiceDetailView(LoginRequiredMixin, DetailView):
#     model = Choice


# class ChoiceDeleteView(LoginRequiredMixin, DeleteView):
#     model = Choice
#     success_url = reverse_lazy('questions:choice-list')

def QuestionCopy(request, pk):
    # form_class = QuestionForm

    question = Question.objects.get(id=pk)
    question.pk = None
    # question.question_text = 'COPY:' + question.question_text
    question.save()
    # new_id = question.id
    # context = {'question':question}

    # if request.method == 'POST':
    #     formset = ChoiceFormSet(request.POST, instance = choice_group)
    #     if formset.is_valid():
    #         formset.save()
    #         return redirect('questions:choice-create', pk = choice_group.id)

    return redirect('questions:question-update', pk=question.id)
    # return render(request, "questions/question_copy.html", context)
    # questions / question_form.html


def QuestionDetail(request, pk):
    question = Question.objects.get(id=pk)
    choice_group = question.choice_group
    correct_choice = question.choice
    # Below is needed to create a Queryset for combining
    correct_choice_qs = Choice.objects.filter(choice_group=choice_group, choice=correct_choice).order_by("?")[:1]
    wrong_choices = Choice.objects.filter(choice_group=choice_group).exclude(choice=correct_choice)
    all_choices = correct_choice_qs | wrong_choices

    all_choices_list = list(all_choices)
    # shuffle(all_choices_list)

    context = {'question': question, 'all_choices': all_choices_list}
    return render(request, "questions/question_detail.html", context)


def QuestionGenerate(request, pk):
    question = Question.objects.get(id=pk)
    choice_group = question.choice_group
    correct_choice = question.choice
    # Below is needed to create a Queryset for combining
    correct_choice_qs = Choice.objects.filter(choice_group=choice_group, choice=correct_choice).order_by("?")[:1]
    wrong_choices = Choice.objects.filter(choice_group=choice_group).exclude(choice=correct_choice).order_by("?")[:4]
    all_choices = correct_choice_qs | wrong_choices

    all_choices_list = list(all_choices)
    shuffle(all_choices_list)

    context = {'question': question, 'all_choices': all_choices_list}
    return render(request, "questions/question_generate.html", context)


def questionCheckAnswer(request, pk):
    question = Question.objects.get(id=pk)
    correct_answer = question.choice.choice
    data = request.POST
    given_answer = data.get('displayed_choices')
    context = {'question': question, 'given_answer': given_answer, 'correct_answer': correct_answer}
    if given_answer == correct_answer:
        messages.add_message(request, messages.INFO, 'CORRECT')
        # return redirect('questions:question-list')
    else:
        messages.add_message(request, messages.INFO, 'WRONG')
    # return redirect('questions:question-update', pk = pk )
    return render(request, 'questions/question_feedback.html', context)

# def choiceDownload(request):
#     resource = ChoiceResource()
#     dataset = resource.export()
#     response = HttpResponse(dataset.csv, content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="choice.csv"'
#     return response
#
# def choiceGroupDownload(request):
#     resource = ChoiceGroupResource()
#     dataset = resource.export()
#     response = HttpResponse(dataset.csv, content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="choice-group.csv"'
#     return response
#
# def questionDownload(request):
#     resource = QuestionResource()
#     dataset = resource.export()
#     response = HttpResponse(dataset.csv, content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="question.csv"'
#     return response

# def choiceUpload(request):
#     if request.method == 'POST':
#         resource = ChoiceResource()
#         dataset = Dataset()
#         new_data = request.FILES['myfile']
#
#         imported_data = dataset.load(new_data.read())
#         result = resource.import_data(dataset, dry_run=True)  # Test the data import
#
#         if not result.has_errors():
#             resource.import_data(dataset, dry_run=False)  # Actually import now
#
#     return render(request, 'questions/choice_upload.html')

# Works for CSV
def questionExportCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="questions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Question Text', 'Question Type', 'Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5', 'Correct Answer', 'Time in seconds'])

    questionSet = Question.objects.filter(review_status='ACCEPTED')
    for question in questionSet:
        question_text = question.question_text
        choice_group = question.choice_group
        correct_choice = question.choice
        # Below is needed to create a Queryset for combining
        correct_choice_qs = Choice.objects.filter(choice_group=choice_group, choice=correct_choice).order_by("?")[:1]
        wrong_choices = Choice.objects.filter(choice_group=choice_group).exclude(choice=correct_choice).order_by("?")[:4]
        count_wrong_choices = wrong_choices.count()
        generated_question = list(correct_choice_qs)
        generated_question.insert(0, question_text)
        generated_question.insert(1, 'Multiple Choice')
        generated_question.extend(list(wrong_choices))
        if count_wrong_choices == 1:
            generated_question.insert(4, '')
            generated_question.insert(5, '')
            generated_question.insert(6, '')
        if count_wrong_choices == 2:
            generated_question.insert(5, '')
            generated_question.insert(6, '')
        if count_wrong_choices == 3:
            generated_question.insert(6, '')
        generated_question.insert(len(generated_question),'1')
        generated_question.insert(len(generated_question), '60')

        # all_choices_list = list(all_choices)

        # shuffle(all_choices_list)

        writer.writerow(generated_question)
    return response

