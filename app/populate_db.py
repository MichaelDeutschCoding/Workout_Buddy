from datetime import timedelta
from app.models import RidingProfile, RunningProfile, WorkoutProfile, TimeOfDay, DirectMessage
from accounts.models import User, Profile, Location
from faker import Faker
from random import choice, randrange, uniform, random, choices

f = Faker()
locations = Location.objects.all()
times = TimeOfDay.objects.all()

pics = {
    'M': ['user_pics/male1.png', 'user_pics/male2.jpeg', 'user_pics/male3.jpeg', 'user_pics/male4.png', ''],
    'F': ['user_pics/female1.jpeg', 'user_pics/female2.jpeg', 'user_pics/female3.jpeg', 'user_pics/female4.jpeg', '']
}


def create_user():
    """Creates one user using data provided by Faker.
    Makes a User object, and a Profile."""
    fake = f.simple_profile()
    first_name, last_name = fake['name'].rsplit(' ', maxsplit=1)
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=fake['username'],
        email=fake['mail']
    )
    new_user.set_password(fake['username'])
    new_user.save()

    new_profile = Profile.objects.get(user=new_user)
    new_profile.location = choice(locations)
    new_profile.birthdate = fake['birthdate']
    new_profile.sex = fake['sex']
    new_profile.image = choice(pics[fake['sex']])
    new_profile.bio = f.paragraph()
    new_profile.save()
    return new_profile


def add_running_profile(user_profile):
    RunningProfile(
        user=user_profile,
        pref_time_of_day=choice(times),
        weekly_volume=randrange(30, 160),
        avg_pace=timedelta(seconds=randrange(210, 420))
    ).save()

def add_riding_profile(user_profile):
    flat_avg = round(uniform(20, 38), 1)
    RidingProfile(
        user=user_profile,
        pref_time_of_day=choice(times),
        weekly_volume=randrange(50, 150),
        flat_avg=flat_avg,
        hill_avg=flat_avg - 4
    ).save()

def add_workout_profile(user_profile):
    WorkoutProfile(
        user=user_profile,
        pref_time_of_day=choice(times),
        workout_duration=randrange(30, 120)
    ).save()


def populate(num):
    """Creates {num} number of new users and randomly assigns them a location.
    Then has a 60% chance of adding a running, riding, and workout profile."""
    for _ in range(num):
        user_profile = create_user()
        if random() > .6:
            add_riding_profile(user_profile)
        if random() > .6:
            add_running_profile(user_profile)
        if random() > .6:
            add_workout_profile(user_profile)

def new_direct_message():
    sender, recipient = choices(Profile.objects.all(), k=2)
    msg = DirectMessage(
        sender=sender,
        recipient=recipient,
        time_sent=f.date_time_this_year(),
        subject=f.sentence(nb_words=4),
        text=f.text()
    )
    msg.save()

