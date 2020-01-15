from django.contrib.auth.models import User
from django.forms import ModelForm, Form, CharField, EmailField, PasswordInput, EmailInput, TextInput, DateInput, \
    Textarea, FileInput, Select
from accounts.models import Profile

class SignupForm(Form):
    username = CharField(widget=TextInput(attrs={
        'class': 'form-control',
    }))
    password = CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
    }))
    email = EmailField(label='Email', widget=EmailInput(attrs={
        'class': 'form-control mb-2',
    }))
    first_name = CharField(widget=TextInput(attrs={
        'class': 'form-control col m-2',
    }))
    last_name = CharField(widget=TextInput(attrs={
        'class': 'form-control col m-2',
    }))

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            msg = f"Sorry, the username '{username}' is already taken."
            self.add_error('username', msg)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        help_texts = {
            'image': "We recommend you use a square image for best results."
        }
        widgets = {
            'bio': Textarea(attrs={'class': "form-control w-75", 'style': "height:100px;"}),
            'location': Select(attrs={'class': "form-control w-75"}),
            'birthdate': DateInput(attrs={'type': 'date', 'class': 'form-control w-75'}),
            'image': FileInput(attrs={'class': "form-control-file w-75"}),
            'sex': Select(attrs={'class': 'form-control w-25'})
        }
