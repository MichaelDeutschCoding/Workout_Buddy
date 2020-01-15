from django.contrib import admin
from .models import RunningProfile, RidingProfile, WorkoutProfile, TimeOfDay, DirectMessage, Route

admin.site.register(RunningProfile)
admin.site.register(RidingProfile)
admin.site.register(WorkoutProfile)
admin.site.register(TimeOfDay)
admin.site.register(DirectMessage)
admin.site.register(Route)
