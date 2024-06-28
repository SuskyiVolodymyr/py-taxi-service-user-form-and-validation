from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class LicenseValidationMixin:
    def clean_license_number(self) -> ValidationError | str:
        license_number = self.cleaned_data["license_number"]
        if (len(license_number) != 8
                or not license_number[:3].isascii()
                or license_number[:3] != license_number[:3].upper()
                or not license_number[3:].isnumeric()):
            raise ValidationError("Driver license must be only 8 characters length,"
                                  " first 3 uppercase letters and last 5 characters must be digits. ")
        return license_number


class DriverCreationForm(UserCreationForm, LicenseValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self) -> ValidationError | str:
        return super().clean_license_number()


class DriverUpdateLicenseForm(forms.ModelForm, LicenseValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> ValidationError | str:
        return super().clean_license_number()


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"