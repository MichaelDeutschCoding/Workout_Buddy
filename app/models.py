from django.db import models
from django.utils.duration import _get_duration_components


class TimeOfDay(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MinSecDurationField(models.DurationField):
    """Custom Field to display duration as only 'MM:SS',
    excluding other data points like hours, days, microseconds."""

    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val is None:
            return ''

        days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
        return '{:02d}:{:02d}'.format(minutes, seconds)


class RidingProfile(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    pref_time_of_day = models.ForeignKey(TimeOfDay, on_delete=models.CASCADE)
    weekly_volume = models.IntegerField(blank=True, null=True)
    flat_avg = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    hill_avg = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ['pref_time_of_day']


class RunningProfile(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    pref_time_of_day = models.ForeignKey(TimeOfDay, on_delete=models.CASCADE)
    weekly_volume = models.IntegerField(null=True, blank=True)
    avg_pace = MinSecDurationField(null=True)

    class Meta:
        ordering = ['pref_time_of_day']


class WorkoutProfile(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    pref_time_of_day = models.ForeignKey(TimeOfDay, on_delete=models.CASCADE)
    workout_duration = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['pref_time_of_day']


class DirectMessage(models.Model):
    sender = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='recipient')
    time_sent = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=63, null=True, blank=True)
    text = models.CharField(max_length=255)
    read = models.BooleanField(default=False)


class Route(models.Model):
    title = models.CharField(max_length=50)
    contributor = models.ForeignKey('accounts.Profile', on_delete=models.DO_NOTHING)
    distance = models.DecimalField(max_digits=4, decimal_places=1)
    elevation = models.PositiveIntegerField()
    description = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    added_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-added_on']

    def __str__(self):
        return f"{self.title} added by {self.contributor} on {self.added_on}"
