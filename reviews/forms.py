from django import forms
from django.forms import TextInput, FileInput, RadioSelect

from . import models


class TicketForm(forms.ModelForm):
    # Our form inherit from ModelForm, it lets the model define the form fields automatically
    class Meta:  # inner class specifies the model for which this form will be used
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'width: 500px;',
                'placeholder': 'Titre',
                'size': 100,
            }),

            'description': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'width: 500px; height: 200px; border: 4px solid #2F4F4F; border-radius: 3px;',
                'placeholder': 'Description',
                'size': 100
            }),

            'image': FileInput(attrs={
                'class': "form-control",
                'style': 'width: 500px;',
                'placeholder': 'Image',
                'size': 100
            })
        }
        required = (
            'title',
            'description',
        )


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        widget=RadioSelect(attrs={'class': 'inline', 'style': 'accent-color: #2F4F4F; border: 3px solid #FFF;'}),
        choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]  # set the Radio Button for the rating
    )

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']
        labels = {
            'rating': 'Note',
            'headline': 'Description',
            'body': 'Commentaire',
        }
        widgets = {
            'headline': TextInput(attrs={
                'class': "form-control",
                'style': 'width: 500px;',
                'placeholder': 'Titre',
                'size': 100
            }),
            'body': TextInput(attrs={
                'class': "form-control",
                'style': 'width: 500px; height: 200px; border: 4px solid #2F4F4F; border-radius: 3px;',
                'placeholder': 'Commentaire',
                'size': 100
            })
        }


class FollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
        labels = {'followed_user': 'suivre'}
