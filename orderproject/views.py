from django.shortcuts import redirect


def home(request):
    if request.user.is_authenticated():
        return redirect('/edit/')
    else:
        return redirect('account_login')
