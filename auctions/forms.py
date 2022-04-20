from django import forms
from django.db.models import Max
# from django.core.exceptions import ValidationError

from .models import User, Category, Listing, Bid, Comment

from decimal import Decimal


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'category', 'name',
            'image', 'start_bid',
            'description'
        ]
        labels = {
            'name': 'Listing name', 'category': 'Category',
            'description': 'Description', 'start_bid': 'Start bid',
            'image': 'Image URL'
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid', 'listing')
        # exclude = ('listing',)
        labels = {'bid': 'Your Bid'}
        widgets = {'listing': forms.HiddenInput()}

    # def __init__(self, *args, **kwargs) -> None:
    #     # self.fields['listing'] = listing #self.data['listing']
    #     # super().__init__(self, *args, **kwargs)
    #     super(BidForm, self).__init__(*args, **kwargs)
    #     self.fields['listing'].widget = forms.HiddenInput()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     new_bid = cleaned_data.get('bid')
    #     listing = cleaned_data.get('listing')
    #     # print(listing)
    #     start_bid = Listing.objects.get(name=listing)
    #     current_bid = Bid.objects.filter(listing=listing).aggregate(Max('bid'))
        
    #     if start_bid and current_bid >= new_bid:
    #         raise forms.ValidationError("Your bid must be higher than previous")

    def clean(self):
        new_bid = self.cleaned_data.get('bid')
        listing = self.cleaned_data.get('listing')
        start_bid = listing.start_bid
        bids = listing.bid_set.order_by('-date_added')
        current_bid = bids[0].bid if bids else start_bid

        if new_bid <= current_bid:
            raise forms.ValidationError(
                "Your bid must be higher than previous"
            )
        # return new_bid

    # def clean_bid(self):
    #     new_bid = self.cleaned_data['bid']
    #     start_bid = self.instance.listing.start_bid
    #     previous_bid = Bid.objects.filter(listing=self.instance.listing
    #         ).aggregate(Max('bid'))
    #     current_bid = previous_bid if previous_bid else start_bid
    #     if new_bid <= current_bid:
    #         raise forms.ValidationError(
    #             'Your bid must be higher than previous'
    #         )
    #     return new_bid

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Comment'}