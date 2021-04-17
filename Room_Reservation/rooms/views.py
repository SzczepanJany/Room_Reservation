from typing import Callable
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views import View
from django.urls import reverse
from rooms.models import Room, Room_Reservation
from django.contrib import messages
from datetime import date, datetime

# Create your views here.
class main(View):
    def get(self, request):
        rooms = Room.objects.order_by('id')
        res_all = Room_Reservation.objects.order_by('res_date')
        if not rooms:
            empty = True
        else:
            empty = False
        return render(request, template_name='main.html', context={'rooms':rooms, 'empty':empty, 'today':datetime.today(), 'res_all':res_all})
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
    def get(self, request, id):
        room = Room.objects.get(id=id)
        reservations = Room_Reservation.objects.filter(room = room, res_date__gte=datetime.today().strftime('%Y-%m-%d')).order_by('res_date')
        return render(request, template_name='room.html', context={'room':room, 'reservations':reservations})
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
        room = Room.objects.get(id=id)
        res_total = Room_Reservation.objects.filter(room = room, res_date__gte=datetime.today().strftime('%Y-%m-%d')).order_by('res_date')
        return render(request, template_name="room_res.html", context={'today':datetime.today(),'res_total':res_total})
    def post(self, request, id):
        room = Room.objects.get(id=id)
        

        res_date = request.POST.get('res_date')
        if res_date < str(datetime.today().strftime('%Y-%m-%d')):
            messages.info(request, f"Cannot book room for the date from the past")
            return redirect(reverse('room_res', args=(id,)))
        res_comm = request.POST.get('comment')
        no_res = False
        try:
            res = Room_Reservation.objects.get(room=room, res_date=res_date)
        except:
            no_res = True
        if no_res:
            reservation = Room_Reservation()
            reservation.res_date = res_date
            reservation.comment = res_comm
            reservation.room = room
            reservation.save()
            return redirect(reverse('rooms'))
        else:
            messages.info(request, f'Room already booked for this date')
            return redirect(reverse('room_res', args=(id,)))

class room_search(View):
    def get(self, request):
        name = request.GET.get('name')
        capacity = request.GET.get('capacity')
        projector = request.GET.get('projector')
        if_projector = request.GET.get('if_projector')
        try:
            capacity = int(capacity)
        except:
            if capacity:
                messages.info(request, f'Check capacity')
                return redirect(reverse('rooms'))
            else:
                pass

        room = Room.objects.none()
        if name:
            room |= Room.objects.filter(name=name).order_by('name')
        if capacity:
            room |= Room.objects.filter(capacity__gte=capacity).order_by('name')
        if if_projector:
            room |= Room.objects.filter(projector=projector=='on').order_by('name')
        res_all = Room_Reservation.objects.order_by('res_date')
        if not room:
            empty = True
        else:
            empty = False
        return render(request, template_name='main.html', context={'rooms':room, 'empty':empty, 'today':datetime.today(), 'res_all':res_all})