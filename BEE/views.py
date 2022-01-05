from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Case run manager account request '
            message = render_to_string('acc_active_email.html', {
            #     managerName
            # 'Shub'
            # fullname
            # 'Satish Dhule'
            # managerEmail
            # 'shubhendra.darwade@credit-suisse.com'
                'fullname' : request.POST.get('fullname'),
                'managername' : request.POST.get('managerName'),
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('managerEmail')
            # email = EmailMessage(
            #             mail_subject, message, to=[to_email]
            # )
            # email.send()
            msg = MIMEText(message)
            msg["From"] = "casemanager-automation@credit-suisse.com"
#            msg["To"] = to_email
            msg["To"] = "satishkumar.dhule@credit-suisse.com"
            msg["Cc"] = "satishkumar.dhule@credit-suisse.com"
            msg["Subject"] = mail_subject
            p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
            p.communicate(msg.as_string())
            #return HttpResponse('Activation link has been sent to your manager. Your Profile will be activated as soon '
            return HttpResponse('Activation link has been sent to Support Team. Your Profile will be activated as soon '
                                'as team confirms by clicking the link.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation..')
    else:
        return HttpResponse('Activation link is invalid!')
