from django import forms

from .models import MarketplaceListing


class MarketplaceListingForm(forms.ModelForm):
    class Meta:
        model = MarketplaceListing
        fields = [
            "title",
            "description",
            "category",
            "character_name",
            "price_or_trade",
            "meeting_location",
            "contact_information",
            "image",
        ]
        widgets = {"description": forms.Textarea(attrs={"rows": 8})}


class StaffMarketplaceListingForm(MarketplaceListingForm):
    class Meta(MarketplaceListingForm.Meta):
        fields = [*MarketplaceListingForm.Meta.fields, "status"]
