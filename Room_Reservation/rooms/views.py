from typing import Callable
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse
from rooms.models import Room
from django.contrib import messages


# Create your views here.
class main(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, template_name='main.html', context={'rooms':rooms})
    def post(self, request):
        pass

class room_add(View):
    def get(self, request):
        return render(request, template_name='room_add.html')
    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        try:
            capacity = int(capacity)
        except:
                messages.info(request, f'Check capacity')
                return redirect(reverse('room_add'))    
        if name and len(name) > 0:
            tmp_name = Room.objects.filter(name = name)
            if not tmp_name and capacity > 0:
                room = Room()
                room.name = name
                room.capacity = capacity
                room.projector = projector == 'on'
                room.save()
                return redirect(reverse('rooms'))
            else:
                messages.info(request, f'Check room name and capacity')
                return redirect(reverse('room_add'))
        else:
            messages.info(request, f'Check room name')
            return redirect(reverse('room_add'))
