
from django import forms
from order.models import Empresa


class SignupForm(forms.Form):
    #first_name = forms.CharField(max_length=30, label='Nombre')
    #last_name = forms.CharField(max_length=30, label='Apellido')
    
    nombre_empresa = forms.CharField(max_length=50, label='Nombre empresa', min_length=6)

    def save(self, user):
        empresa_name = self.cleaned_data['nombre_empresa']
        empresa = Empresa(name=empresa_name)
        empresa.save()
        
        user.get_profile().empresa = empresa
        user.get_profile().save()