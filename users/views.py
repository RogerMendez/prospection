from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.conf import settings

from datetime import timedelta, datetime

from django.contrib.auth.models import User
from prospection.general_utility import create_code_activation, send_email
from users.models import ActivationCode, Person
from users.form import EmailForm, UsernameForm, PersonForm

def index(request):

    return render(request, 'index.html', {

    })

def user_register(request):
    if request.method == 'POST':
        formuser  = UserCreationForm(request.POST)
        formemail = EmailForm(request.POST)
        if formuser.is_valid() and formemail.is_valid():
            user = formuser.save()
            email = formemail.cleaned_data['email']
            user.email = email
            user.is_active = False
            user.save()
            activation = ActivationCode.objects.create(
                code = create_code_activation(),
                user = user,
            )
            html = render_to_string('mail/send_code.html', {
                'url':settings.ADDREES,
                'code':activation.code,
                'user':user,
            })
            send_email(email, html)

            sms = "Registro Realizado Correctamente"
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(index))
    else:
        formuser = UserCreationForm()
        formemail = EmailForm()
    return render(request, 'users/new.html', {
        'formuser':formuser,
        'formemail':formemail,
    })

def users_activate(request, code, user_id):
    if ActivationCode.objects.filter(user_id = user_id, state = True, code = code):
        user = User.objects.get(id = user_id)
        code = ActivationCode.objects.get(user = user, state = True, code = code)
        user.is_active = True
        user.save()
        code.state = False
        code.save()
        sms = 'Cuenta Activada Correctamente'
        messages.success(request, sms)
    else:
        sms = 'Usted No Se Registro'
        messages.info(request, sms)
    return HttpResponseRedirect('/')

def user_login(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse(user_notification))
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            access = authenticate(username=username, password=password)
            if access is not None:
                if access.is_active:
                    end_joined = access.date_joined + timedelta(days = 30)
                    today = datetime.now()
                    #COMPROVAR SI REALIZO EL PAFO U OTRA FORMA DE CONTROL PARA QUE NO SEA FREE
                    if today.strftime("%Y-%m-%d %H:%M") <= end_joined.strftime("%Y-%m-%d %H:%M"):
                        login(request, access)
                        if 'next' in request.GET:
                            msm = "Inicio de Sesion Correcto <strong>Gracias Por Su Visita</strong>"
                            messages.add_message(request, messages.INFO, msm)
                            return HttpResponseRedirect(str(request.GET['next']))
                        else:
                            msm = "Inicio de Sesion Existoso <strong>Gracias Por Su Visita</strong>"
                            messages.add_message(request, messages.SUCCESS, msm)
                            return HttpResponseRedirect(reverse(user_notification))
                    else:
                        sms = 'Su Cuenta ya Caduco '
                        messages.warning(request, sms)
                else:
                    sms = "Su Cuenta No Esta Activada <strong>Verifique su Correo Electronico Para Activar La Cuenta</strong>"
                    messages.warning(request, sms)
                    return HttpResponseRedirect('/')
            else:
                msm = "Usted No Es Usuario Del Sistema - <strong>Registrate</strong>"
                messages.add_message(request, messages.ERROR, msm, 'danger')
                return HttpResponseRedirect(reverse(user_login))
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html',{
        'form':form,
    })

@login_required(login_url='/login')
def user_logout(request):
    msm = "Sesion Terminada Correctamente <strong>Vuelva Pronto</strong>"
    messages.warning(request, msm)
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def user_notification(request):
    return render(request, 'users/index.html')

@login_required(login_url='/login')
def user_changepassword(request):
    if request.method == 'POST' :
        form = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(user_notification))
    else:
        form= AdminPasswordChangeForm(user=request.user)
    return  render(request, 'users/change_pass.html', {
        'form' :form,
    })

@login_required(login_url='/login')
def user_changeusername(request):
    if request.method == 'POST' :
        form = UsernameForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            sms = 'Nombre De Usuario Modificado Correctamente'
            messages.info(request, sms)
            return HttpResponseRedirect(reverse(user_notification))
    else:
        form= UsernameForm(instance=request.user)
    return  render(request, 'users/change_username.html', {
        'form' :form,
    })

def user_sendcoderesetpass(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email = email):
            user = User.objects.get(email = email)
            url = settings.ADDREES
            activation = ActivationCode.objects.create(
                code = create_code_activation(),
                user = user,
                description = 'Reset Pass',
            )
            html = render_to_string('mail/send_code_reset_pass.html',{
                'code':activation.code,
                'url':url,
                'user':user,
            })
            send_email(email, html, subject='Recuperacion de Contraseña')
            sms = u"Un mensage fue enviado a su correo electronico para recuperar la contraseña"
            messages.add_message(request, messages.INFO, sms)
            return HttpResponseRedirect('/')
        else:
            sms = "El Correo Eletronico no esta registrado"
            messages.warning(request, sms)
            return HttpResponseRedirect(reverse(user_register))
    return render(request, 'users/send_resetpass.html')

def user_recoverpass(request, user_id, code):
    if ActivationCode.objects.filter(user_id = user_id, state = True, code = code, description='Reset Pass'):
        activation = ActivationCode.objects.get(user_id = user_id, state = True, code = code, description='Reset Pass')
        user = User.objects.get(id = user_id)
        envio = activation.send_time + timedelta(hours=24)
        today = datetime.now()
        if envio.strftime("%Y-%m-%d %H:%M") >= today.strftime("%Y-%m-%d %H:%M"):
            if request.method == 'POST':
                form = AdminPasswordChangeForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()
                    activation.state = False
                    activation.save()
                    sms = "Contraseña Cambiada Correctamente"
                    messages.success(request, sms)
                    return HttpResponseRedirect(reverse(user_login))
            else:
                form = AdminPasswordChangeForm(user=user)
            return render(request, 'users/reset_pass.html', {
                'form':form,
            })
        else:
            sms = "El Enlace ya expiro por favor solicite uno nuevo"
            messages.error(request, sms, 'danger')
            return HttpResponseRedirect(reverse(user-user-user_sendcoderesetpass))
    else:
        sms = "Enlace no Valido"
        messages.error(request, sms, 'danger')
        return HttpResponseRedirect('/')

@login_required(login_url='/login')
def my_information(request):
    if Person.objects.filter(user = request.user):
        person = Person.objects.get(user = request.user)
        return render(request, 'users/my_information.html',{
            'person':person,
        })
    else:
        if request.method == 'POST':
            form = PersonForm(request.POST)
            if form.is_valid():
                person = form.save(commit=False)
                person.user = request.user
                person.save()
                sms = 'Información Registrada Correctamente'
                messages.success(request, sms)
                return HttpResponseRedirect(reverse(my_information))
        else:
            form = PersonForm()
    return render(request, 'users/new_person.html', {
        'form':form,
    })

@login_required(login_url='/login')
def modify_information(request):
    person = Person.objects.get(user = request.user)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            sms = 'Información Registrada Correctamente'
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(my_information))
    else:
        form = PersonForm(instance=person)
    return render(request, 'users/update_information.html', {
        'form':form,
    })