from .models import RunningProfile, RidingProfile, WorkoutProfile, DirectMessage, Route
from django.forms import ModelForm, Select, NumberInput, Textarea, TimeInput, TextInput


class WorkoutForm(ModelForm):
    class Meta:
        model = WorkoutProfile
        exclude = ['user']
        labels = {
            'pref_time_of_day': 'Preferred Time of Day',
            'workout_duration': "Typical Workout Duration (in minutes)"
        }

        widgets = {
            'pref_time_of_day': Select(attrs={'class': "form-control w-50"}),
            'workout_duration': NumberInput(attrs={'class': "form-control w-50"}),
        }


class RidingForm(ModelForm):
    class Meta:
        model = RidingProfile
        exclude = ['user']
        labels = {
            'pref_time_of_day': 'Preferred Time of Day',
            'weekly_volume': "Typical Weekly Volume (in km)",
            'flat_avg': "Average Speed in km/h on a flat ride",
            'hill_avg': "Average Speed in km/h on a hilly ride"
        }
        widgets = {
            'pref_time_of_day': Select(attrs={'class': "form-control w-50"}),
            'weekly_volume': NumberInput(attrs={'class': "form-control w-50"}),
            'flat_avg':  NumberInput(attrs={'class': "form-control w-50"}),
            'hill_avg':  NumberInput(attrs={'class': "form-control w-50"}),
        }


class RunningForm(ModelForm):
    class Meta:
        model = RunningProfile
        exclude = ['user']
        labels = {
            'pref_time_of_day': 'Preferred Time of Day',
            'weekly_volume': "Typical Weekly Volume (in km)",
            'avg_pace': "Average Pace (min/km)"
        }
        widgets = {
            'pref_time_of_day': Select(attrs={'class': "form-control w-50"}),
            'weekly_volume': NumberInput(attrs={'class': "form-control w-50"}),
            'avg_pace': TimeInput(attrs={'class': "form-control w-50"}),

        }

class MessageForm(ModelForm):
    class Meta:
        model = DirectMessage
        fields = ['recipient', 'text', 'sender', 'subject']
        widgets = {
            'text': Textarea(attrs={'class': "form-control w-75 mt-3", 'style': "height:100px;"}),
            'subject': TextInput(attrs={'class': "form-control w-75", 'placeholder': 'Subject'}),
            'recipient': Select(attrs={'class': "form-control w-25"})
        }


class RouteForm(ModelForm):
    class Meta:
        model = Route
        exclude = ['contributor', 'added_on']
