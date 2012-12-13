from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated():
        return render(request, "home.html")
    else:
        return redirect('account_login')