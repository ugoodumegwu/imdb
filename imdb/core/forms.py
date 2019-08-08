from django import forms
from .models import Movie
from .models import Vote, MovieImage
from django.contrib.auth import get_user_model
from django.conf import settings

class VoteForm(forms.ModelForm):
    # To prevent Users for voting for other users we must add more code to this form
    # Note when you set any field attribute disabled=True that particular field will not be able to post data
    user = forms.ModelChoiceField( queryset=get_user_model().objects.all(), widget=forms.HiddenInput)
    movie = forms.ModelChoiceField( queryset=Movie.objects.all(), widget=forms.HiddenInput)
    value = forms.ChoiceField(label='Vote', widget=forms.RadioSelect, choices=Vote.VALUE_CHOICES)


    class Meta:
        model = Vote
        fields = ('value', 'user', 'movie')



class ImageForm(forms.ModelForm):

    user = forms.ModelChoiceField( widget=forms.HiddenInput, queryset=get_user_model().objects.all())
    movie = forms.ModelChoiceField( widget=forms.HiddenInput,  queryset=Movie.objects.all())

    class Meta:
        model = MovieImage
        fields = ('user', 'movie', 'image')