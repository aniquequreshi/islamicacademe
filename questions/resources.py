from import_export import resources
from .models import Choice, ChoiceGroup, Question
from django.contrib.auth.models import User

class ChoiceResource(resources.ModelResource):
    class Meta:
        model = Choice

class ChoiceGroupResource(resources.ModelResource):
    class Meta:
        model = ChoiceGroup

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')