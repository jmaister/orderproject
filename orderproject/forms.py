
from django.forms.models import ModelForm
from order.models import OrderUser


class OrderUserForm(ModelForm):

    # company = forms.CharField(max_length=50, label='Company Name', min_length=6)

    def save(self, user):
        company = self.cleaned_data['company']

        user.company = company
        user.save()

    class Meta:
        model = OrderUser
        fields = ('email', 'company', 'id_number', 'address')
