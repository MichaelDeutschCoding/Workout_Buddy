import django_filters
from django.forms import TextInput, Select
from django_filters.widgets import RangeWidget

from accounts.models import Location
from app.models import RidingProfile, WorkoutProfile, RunningProfile, TimeOfDay


class BaseSportFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name='user__user__username',
        label="Username",
        lookup_expr='icontains',
        widget=TextInput(attrs={'class': "form-control", 'placeholder': "Username"})
    )
    location = django_filters.ModelChoiceFilter(
        field_name='user__location',
        queryset=Location.objects.all(),
        label='Location',
        widget=Select(attrs={'class': "form-control"}),
        empty_label='Choose a Location',
    )
    time_of_day = django_filters.ModelChoiceFilter(
        field_name='pref_time_of_day',
        queryset=TimeOfDay.objects.all(),
        empty_label='Preferred Time of Day',
        widget=Select(attrs={'class': "form-control"})
    )


class RidingFilter(BaseSportFilter):

    hills = django_filters.RangeFilter(
        field_name='hill_avg',
        widget=RangeWidget(attrs={
            'class': "form-control form-control-sm col",
            'placeholder': "Speed in kph",
            'style': 'margin-left: 10px; margin-right: 10px;'
        })
    )
    flats = django_filters.RangeFilter(
        field_name='flat_avg',
        widget=RangeWidget(attrs={
            'class': "form-control form-control-sm col",
            'placeholder': "Speed in kph",
            'style': 'margin-left: 10px; margin-right: 10px;'
        })
    )
    weekly_volume = django_filters.NumberFilter(
        field_name='weekly_volume',
        lookup_expr='gt',
        widget=TextInput(attrs={
            'class': "form-control form-control col",
            'placeholder': "Minimum Weekly Volume (in km)"
        })
    )

    class Meta:
        model = RidingProfile
        fields = []


class WorkoutFilter(BaseSportFilter):

    class Meta:
        model = WorkoutProfile
        fields = []


class RunningFilter(BaseSportFilter):

    pace = django_filters.RangeFilter(
        field_name='avg_pace',
        widget=RangeWidget(attrs={
            'class': "form-control form-control-sm col-2",
            'placeholder': "Pace per km (MM:SS)",
            'style': 'margin-left: 10px; margin-right: 10px;'
        })
    )
    weekly_volume = django_filters.NumberFilter(
        field_name='weekly_volume',
        lookup_expr='gt',
        widget=TextInput(attrs={
            'class': "form-control form-control col",
            'placeholder': "Minimum Weekly Volume (in km)"
        })
    )

    class Meta:
        model = RunningProfile
        fields = []
