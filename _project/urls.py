
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('reservation/', include('reservation.urls', namespace='reservation')),
    path('admin/', admin.site.urls),

]
