from django.contrib.admin.forms import ERROR_MESSAGE
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.fields import BooleanField
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy


## http://tryolabs.com/Blog/2012/06/18/django-administration-interface-non-staff-users/

class UserAdminAuthenticationForm(AuthenticationForm):
    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff.
    """
    this_is_the_login_form = BooleanField(widget=HiddenInput,
                                initial=1,
                                error_messages={'required': ugettext_lazy(
                                "Please log in again, because your session has"
                                " expired.")})
 
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE
         
        if username and password:
            self.user_cache = authenticate(username=username,
            password=password)
            if self.user_cache is None:
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username?
                    # Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your "
                                        "username."
                                        " Try '%s' instead.") % user.username
                raise ValidationError(message)
            # Removed check for is_staff here!
            elif not self.user_cache.is_active:
                raise ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data