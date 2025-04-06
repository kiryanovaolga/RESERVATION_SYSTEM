from django.urls import path
from reservation import views


app_name = 'reservation'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('services_view/', views.services_view, name='services_view'),
    
    path('client-page/', views.client_page, name='client_page'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('specialist-page/', views.specialist_page, name='specialist_page'),
    
    path('team_view/', views.team_view, name='team_view'),
    path('services_list/', views.services_list, name='services_list'),
    path('view_specialists/', views.view_specialists, name='view_specialists'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('view_clients/', views.view_clients, name='view_clients'),
    path('view_clients_for_specialist/', views.view_clients_for_specialist, name='view_clients_for_specialist'),
    
    path('add_specialists/', views.add_specialist, name='add_specialists'),
    path('add_clients/', views.add_clients, name='add_clients'),
    path('add_service/', views.add_service, name='add_service'),
    
    path('delete_specialists/<int:number>/', views.delete_specialists, name='delete_specialists'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    
    path('client/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('specialist/edit/<int:specialist_id>/', views.edit_specialist, name='edit_specialist'),
    path('service/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    
    path('choose_specialist/', views.choose_specialist, name='choose_specialist'),
    path('choose_service/', views.choose_service, name='choose_service'),
    path('choose_datetime/', views.choose_datetime, name='choose_datetime'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('booking_success/', views.booking_success, name='booking_success'),

    path('client_appointment/', views.client_appointments, name='client_appointment'),
    path('specialist_appointment/', views.specialist_appointments, name='specialist_appointment'),
    path('booking_detail/<int:number>/', views.booking_details, name='booking_detail'),
    path('booking_detail_specialist/<int:number>/', views.specialist_booking_details, name='booking_detail_specialist'),
    path('booking_cancel/<int:number>/', views.booking_cancel, name='booking_cancel'),
]