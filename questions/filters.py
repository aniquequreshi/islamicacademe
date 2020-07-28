import django_filters
from django_filters import FilterSet, DateFromToRangeFilter
from django_filters.widgets import RangeWidget

from .models import Question


class QuestionFilter(FilterSet):
    class Meta:
        model = Question
        # exclude = ['tags']
        fields = {
            # 'tags': ['contains'],
            'review_status': ['exact'],
        }#is not working, but still need it
        # last_modified_date_range = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
