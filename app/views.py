from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from accounts.models import Location
from app.filters import RidingFilter, WorkoutFilter, RunningFilter
from app.forms import RunningForm, RidingForm, WorkoutForm, MessageForm
from app.models import DirectMessage, Route
from django.db.models import Q

def landing(request):
    return render(request, 'app/landing.html')

@login_required
def home(request):
    profile = request.user.profile
    new_msgs = DirectMessage.objects.filter(recipient=profile, read=False).count()
    return render(request, 'app/home.html', {'new_msgs': new_msgs})


form_fetcher = {
    'riding': RidingForm,
    'running': RunningForm,
    'workout': WorkoutForm
}

@login_required
def add_sport_profile(request, sport_type):
    if sport_type not in form_fetcher:
        messages.error(request, "Sorry, we don't have that type of activity yet.")
        return redirect(reverse('home'))
    profile = request.user.profile
    if not profile.location:
        messages.error(request, 'You must edit your profile to include a location before you may add a sport profile.')
        return redirect(reverse('accounts:edit-profile'))
    if request.method == 'POST':
        form = form_fetcher[sport_type](request.POST)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = profile
            new_profile.save()
            messages.info(request, f"{sport_type} profile added.")
            return redirect(reverse('home'))

    else:
        form = form_fetcher[sport_type](instance=profile)

    return render(request, 'app/add_sport_profile.html', {
        'sport_type': sport_type,
        'form': form
    })

@method_decorator(login_required, name='dispatch')
class BaseFilterView(FilterView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        loc_id = self.request.GET.get('location', None)
        if loc_id:
            location = Location.objects.get(pk=loc_id)
        elif loc_id == '':
            location = 'Israel'
        else:
            location = self.request.user.profile.location

        context['location_title'] = location
        return context

    def get_filterset_kwargs(self, filterset_class):
        user_location = self.request.user.profile.location

        kwargs = super().get_filterset_kwargs(filterset_class)
        if kwargs['data'] is None:
            kwargs['data'] = {'location': user_location}
        return kwargs


class RidingFilterView(BaseFilterView):
    filterset_class = RidingFilter
    template_name = 'app/riding_profiles.html'


class RunningFilterView(BaseFilterView):
    filterset_class = RunningFilter
    template_name = 'app/running_profiles.html'

class WorkoutFilterView(BaseFilterView):
    filterset_class = WorkoutFilter
    template_name = 'app/workout_profiles.html'


@login_required
def send_message(request):

    if request.method == 'POST':
        form = MessageForm(request.POST)
        form.fields['sender'].required = False
        if form.is_valid():
            msg = form.save(commit=False)
            recipient = msg.recipient.user.username
            msg.sender = request.user.profile
            msg.save()
            messages.info(request, f'Message sent to {recipient}.')
            return redirect(reverse('home'))
    form = MessageForm()

    return render(request, 'app/send_message.html', {'form': form})


@login_required
def view_messages(request):
    me = request.user.profile
    dm_list = DirectMessage.objects.filter(Q(sender=me) | Q(recipient=me)).order_by('-time_sent')
    return render(request, 'app/messages.html', {'dm_list': dm_list})

@login_required
def inbox(request):
    dm_list = DirectMessage.objects.filter(recipient=request.user.profile)
    return render(request, 'app/messages.html', {'dm_list': dm_list})

@login_required
def read_message(request, message_id):
    try:
        msg = DirectMessage.objects.get(pk=message_id)
    except DirectMessage.DoesNotExist:
        messages.error(request, "That message does not exist.")
        return redirect(reverse('messages'))
    profile = request.user.profile
    if not (msg.sender == profile or msg.recipient == profile):
        messages.error(request, 'You do not have permission to read that message.')
        return redirect(reverse('messages'))

    msg.read = True
    msg.save()
    return render(request, 'app/directmessage.html', {'message': msg})


class RouteList(ListView):
    model = Route


class RouteCreate(LoginRequiredMixin, CreateView):
    model = Route
    fields = ['title', 'distance', 'elevation', 'description', 'link']

    def form_valid(self, form):
        form.instance.contributor = self.request.user.profile
        messages.info(self.request, 'Route added. Thanks for your contribution.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all-routes')
