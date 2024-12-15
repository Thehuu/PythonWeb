from django.http import JsonResponse
from django.shortcuts import render
from .models import ReliefLocation, Incident
from .forms import ReliefPointForm

def show_map(request):
    form = ReliefPointForm()
    locations = ReliefLocation.objects.filter(status='approved')
    locations_data = [{'name': loc.name, 'mobile': loc.mobile, 'latitude': float(loc.latitude), 'longitude': float(loc.longitude), 'description': loc.description} for loc in locations]

    tngt_count = Incident.objects.filter(incident_type='TNGT').count()
    drowning_count = Incident.objects.filter(incident_type='DROWNING').count()
    fire_count = Incident.objects.filter(incident_type='FIRE').count()
    disaster_count = Incident.objects.filter(incident_type='DISASTER').count()

    context = {
        'form': form,
        'locations': locations_data,
        'tngt_count': tngt_count,
        'drowning_count': drowning_count,
        'fire_count': fire_count,
        'disaster_count': disaster_count,
    }

    return render(request, 'map/map.html', context)

def save_location(request):
    if request.method == 'POST':
        form = ReliefPointForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid request'})

