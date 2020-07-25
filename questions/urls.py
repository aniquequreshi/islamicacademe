from django.urls import path

from . import views
from .views import choiceCreateView, questionExportCSV

app_name = 'questions'
urlpatterns = [
    path('ajax/load-choices/', views.load_choices, name='ajax_load_choices'),

    path('create/', views.QuestionCreateView.as_view(), name='question-create'),
    path('update/<int:pk>/', views.QuestionUpdateView.as_view(), name='question-update'),
    path('list/', views.QuestionListView.as_view(), name='question-list'),
    path('list/all/', views.QuestionListAllView.as_view(), name='question-list-all'),  #see everyone's questions, newest first
    # path('list/next/', views.QuestionListNextView.as_view(), name='question-list-next'),  #see everyone's oldest five questions
    path('detail/<int:pk>/', views.QuestionDetail, name='question-detail'),
    # path('delete/<int:pk>/', views.DeleteView.as_view(), name='question-delete'),

    path('admin-update/<int:pk>/', views.QuestionAdminUpdateView.as_view(), name='question-admin-update'),

    path('choice/group/create/', views.ChoiceGroupCreateView.as_view(), name='choice-group-create'),
    path('choice/group/update/<int:pk>/', views.ChoiceGroupUpdateView.as_view(), name='choice-group-update'),
    # path('choice/group/list/', views.ChoiceGroupListView.as_view(), name='choice-group-list'),
    # path('choice/group/detail/<int:pk>/', views.ChoiceGroupDetailView.as_view(), name='choice-group-detail'),
    # path('choice/group/delete/<int:pk>/', views.ChoiceGroupDeleteView.as_view(), name='choice-group-delete'),

    path('choice/create/<int:pk>/', choiceCreateView, name='choice-create'),
    # path('choice/update/<int:pk>/', views.ChoiceUpdateView.as_view(), name='choice-update'),
    # path('choice/list/', views.ChoiceListView.as_view(), name='choice-list'),
    # path('choice/detail/<int:pk>/', views.ChoiceDetailView.as_view(), name='choice-detail'),
    # path('choice/delete/<int:pk>/', views.ChoiceDeleteView.as_view(), name='choice-delete'),

    path('subject/create/', views.SubjectCreateView.as_view(), name='subject-create'),
    path('subject/update/<int:pk>/', views.SubjectUpdateView.as_view(), name='subject-update'),

    path('copy/<int:pk>/', views.QuestionCopy, name='question-copy'),
    path('generate/<int:pk>/', views.QuestionGenerate, name='question-generate'),
    path('answer/check/<int:pk>/', views.questionCheckAnswer, name='question-answer-check'),

    # path('choice/download/', views.choiceDownload, name='choice-download'),
    # path('choice/group/download/', views.choiceGroupDownload, name='choice-group-download'),
    # path('question/download/', views.questionDownload, name='question-download'),
    # path('answer/display/', views.questionAnswerDisplay, name='question-answer-display'),
    # path('choice/upload/', views.choiceUpload, name='choice-upload'),

    path('download/csv', views.questionExportCSV, name='question-export-csv'),
    path('question/subject/update/<int:pk>/', views.QuestionSubjectUpdateView.as_view(), name='question-subject-update'),
]