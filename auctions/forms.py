from django import forms
from .models import Auction, Bid, Comment


class AuctionForm(forms.ModelForm):
    """
    Creates the form for creating a new auction.
    """

    class Meta:
        """
        Django uses Meta class to define form meta attributes.
        It must be named Meta, so Django can process it and create a form.
        """
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


class BidForm(forms.ModelForm):
    """
    Creates the form for bidding on the auction listing page
    """

    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    """
    Creates the form for commenting on the auction listing page
    """

    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control mb-3'}),
        }
