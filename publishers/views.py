# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string

from publishers.models import Publishers, Dates
from publishers.form import PublishersForm, DatesForm

@login_required(login_url='/login')
def index(request):
    publishers = Publishers.objects.filter(user=request.user)
    return render(request, 'publishers/index.html', {
        'publishers':publishers,
    })

@login_required(login_url='/login')
def new_publisher(request):
    if request.method == 'POST':
        form = PublishersForm(request.POST)
        if form.is_valid():
            publisher = form.save(commit=False)
            publisher.user = request.user
            publisher.save()
            sms = 'Publicaciòn Creada Correctamente'
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(index))
    else:
        form = PublishersForm()
    return render(request, 'publishers/new_publisher.html', {
        'form':form,
    })

@login_required(login_url='/login')
def dates_publisher(request, publisher_id):
    publisher = get_object_or_404(Publishers, pk = publisher_id)
    dates = Dates.objects.filter(publisher = publisher)
    if request.method == 'POST':
        form = DatesForm(request.POST)
        if form.is_valid():
            date = form.save(commit=False)
            date.publisher = publisher
            date.save()
            sms = 'Fecha Agregada Correctamente'
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(dates_publisher, args={publisher.id,}))
    else:
        form = DatesForm()
    return render(request, 'publishers/dates_publisher.html',{
        'publisher':publisher,
        'dates':dates,
        'form':form,
    })

@login_required(login_url='/login')
def ends_dates_publisher(request, publisher_id):
    publisher = get_object_or_404(Publishers, pk = publisher_id)
    publisher.state = True
    publisher.save()
    sms = 'Agregacion de Fechas Realizada Correctamente'
    messages.success(request, sms)
    return HttpResponseRedirect(reverse(dates_publisher, args=[publisher.id, ]))