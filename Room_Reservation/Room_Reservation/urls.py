"""Room_Reservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rooms.views import main, room_add, room, room_modify, room_del, room_res


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', main.as_view(), name='rooms'),
    path('room/add/', room_add.as_view(), name='room_add'),
    path('room/<int:id>', room.as_view(), name='room'),
    path('room/modify/<int:id>', room_modify.as_view(), name='room_mod'),
    path('room/delete/<int:id>', room_del.as_view(), name='room_del'),
    path('room/reserve/<int:id>', room_res.as_view(), name='room_res'),

]
