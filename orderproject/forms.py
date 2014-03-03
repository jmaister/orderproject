
from django import forms
from order.models import Company


class SignupForm(forms.Form):

    company_name = forms.CharField(max_length=50, label='Company Name', min_length=6)

    def save(self, user):
        company_name = self.cleaned_data['company_name']
        company = Company(name=company_name)
        company.save()

        user.company = company
        user.save()
