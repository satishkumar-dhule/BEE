from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('casemanager_home')
    else:
        return render(request, 'caseapplication/welcome.html')
