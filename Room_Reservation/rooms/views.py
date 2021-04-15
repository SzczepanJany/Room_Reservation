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
        rooms = Room.objects.order_by('id')

        if not rooms:
            empty = True
        else:
            empty = False
        return render(request, template_name='main.html', context={'rooms':rooms, 'empty':empty})
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


class room(View):
    def get(self, request):
        pass
    def post(self, request):
        pass


class room_modify(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, template_name="room_mod.html", context={'room':room})
    def post(self, request, id):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        try:
            capacity = int(capacity)
        except:
                messages.info(request, f'Check capacity')
                return redirect(reverse('room_mod', args=(id,)))    
        if name and len(name) > 0:
            tmp_name = Room.objects.filter(name = name).exclude(id=id)
            if not tmp_name and capacity > 0:
                room = Room.objects.get(id=id)
                room.name = name
                room.capacity = capacity
                room.projector = projector == 'on'
                room.save()
                return redirect(reverse('rooms'))
            else:
                messages.info(request, f'Check room name and capacity')
                return redirect(reverse('room_mod', args=(id,)))
        else:
            messages.info(request, f'Check room name')
            return redirect(reverse('room_add', args=(id,)))


class room_del(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        room.delete()
        messages.info(request, f'Room "{room.name}" with id: "{room.id}" was deleted')
        return redirect(reverse('rooms'))


class room_res(View):
    def get(self, request, id):
        pass
    def post(self, request, id):
        pass