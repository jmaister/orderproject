from django.utils.translation import to_locale, get_language
from orderproject import settings  # import the settings file


def settings_access(request):

    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'settings': settings,
            'LOCALE': to_locale(get_language())}
