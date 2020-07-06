import django_filters
from django_filters import FilterSet, DateFromToRangeFilter
from django_filters.widgets import RangeWidget

from .models import Question


class QuestionFilter(FilterSet):
    last_modified = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Question
        # exclude = ['review_status']
        fields = ['review_status'] #is not working, but still need it
        last_modified_date_range = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
