from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm # built in Django form, takes care of pw hashing
from django.contrib.auth.models import User # for authentication
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
            }
    # styles fields
    def __init__(self, *args, **kwargs):
        # override super
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # apply class 'input' to each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'bio', 'headline', 'profile_image', 'social_github', 'social_linkedin', 'social_twitter', 'social_stackoverflow', 'social_website' ]

        # styles fields
    def __init__(self, *args, **kwargs):
        # override super
        super(ProfileForm, self).__init__(*args, **kwargs)
        # apply class 'input' to each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        # lists all fields from Skill model on form
        fields = '__all__'
        # excludes owner field which we don't want on form
        exclude = ['owner']
        # styles fields
    def __init__(self, *args, **kwargs):
        # override super
        super(SkillForm, self).__init__(*args, **kwargs)
        # apply class 'input' to each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        # override super
        super(MessageForm, self).__init__(*args, **kwargs)
        # apply class 'input' to each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

