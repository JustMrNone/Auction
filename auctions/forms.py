from django import forms

from .models import *


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ListingForm(forms.ModelForm):
    class Meta:
        model = auction_listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'image_url': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Listing'))

        # Define character limits for the input fields
        self.fields['title'].widget.attrs['maxlength'] = 100
        self.fields['description'].widget.attrs['maxlength'] = 20000

        # Define minimum lengths for the input fields
        self.fields['title'].widget.attrs['minlength'] = 5
        self.fields['description'].widget.attrs['minlength'] = 30