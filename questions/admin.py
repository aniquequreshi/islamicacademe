from django.contrib import admin
from import_export.admin import ImportExportModelAdmin  # django-import-export

from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Question, Subject, Level, ChoiceGroup, Choice

# admin.site.register(Question)
# admin.site.register(Subject)
admin.site.register(Level)


# admin.site.register(ChoiceGroup)
# admin.site.register(Choice)

@admin.register(Choice)
class ChoiceAdmin(ImportExportModelAdmin):
    class Meta:
        pass
        # model = Choice
        # fields = ('choice', 'choice_group')


@admin.register(ChoiceGroup)
class ChoiceGroupAdmin(ImportExportModelAdmin):
    class Meta:
        pass


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    class Meta:
        pass


@admin.register(Subject)
class QuestionAdmin(ImportExportModelAdmin):
    class Meta:
        pass


admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    class Meta:
        pass
