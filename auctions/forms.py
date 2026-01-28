from django import forms
from .models import Auction


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'image_url', 'bid', 'is_active', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'bid': forms.NumberInput(attrs={'class': 'form-control', 'label': 'Starting bid'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_url'].required = False
        self.fields['category'].required = False

        if self.instance and self.instance.pk:
            self.fields['bid'].widget.attrs['readonly'] = True
            self.fields['image_url'].required = False
            self.fields['category'].required = False

    def clean_image_url(self):
        data = self.cleaned_data['image_url']
        if not data:
            return "https://shorturl.at/Tuo6N"
        return data
