# pages/views
from django.shortcuts import render
from events.models import Event
from loans.models import Device
from django.shortcuts import render_to_response

def home_event(request):
    try:
        current_event = Event.objects.latest()
    except Event.DoesNotExist:
        current_event = None
    return render(request, 'pages/home_event.html', {'current_event': current_event})

def home(request):
    #try:
    #    devices = Device.objects.all()
    #except Device.DoesNotExist:
    #    raise Http404
    #return render(request, 'pages/home.html', {'devices': devices})
    return render(request, 'pages/home.html')
    #return render_to_response('pages/home.html', locals())
