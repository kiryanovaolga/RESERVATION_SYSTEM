
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/reservation/')),
    path('reservation/', include('reservation.urls', namespace='reservation')),
    path('admin/', admin.site.urls),

]
