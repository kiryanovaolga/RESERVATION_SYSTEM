from datetime import datetime, timedelta
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth import authenticate, login as auth_login, logout
from reservation.models import Service, Booking, User, Message, AbstractUser
from reservation.forms import UserForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.timezone import now
from django.utils import timezone



def login_view(request):
    error = '' 
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect('reservation:admin_page')
            elif user.role == 'specialist':
                return redirect('reservation:specialist_page')
            elif user.role == 'client':
                return redirect('reservation:client_page')
            else:
                return redirect('home')
        else:
            error = 'Wrong username or password!'
            
    return render(request, 'registration/login.html', {'error': error})



def logout_view(request):
    logout(request)
    return redirect('reservation:login')


def services_view(request):
    services = Service.objects.all()
    return render(request, 'reservation/services_for_quests.html', {'services':services})



def specialist_page(request):
    if request.user.is_authenticated:
        return render (request, 'specialist/specialist_dashboard.html',{'user': request.user})
    else:
        return redirect('reservation:home')


def client_page(request):
    if request.user.is_authenticated:
        services = Service.objects.all()
        return render (request, 'client/client_dashboard.html', {'user': request.user, 'services':services})
    else:
        return redirect('reservation:home')


def admin_page(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render (request, 'admin/admin_dashboard.html')
    else:
        return redirect('reservation:home')


def services_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        services = Service.objects.all()
        return render(request, 'admin/services_list.html', {'services':services })
    else:
        return redirect('reservation:home')



def add_service(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            title= request.POST.get('title')
            desc = request.POST.get('desc')
            price = request.POST.get('price')
            specialists_ids = request.POST.getlist('specialists')
            service = Service.objects.create(
                title=title,
                description= desc,
                price =price,                        
)   
            if specialists_ids:
                selected_specialists = User.objects.filter(id__in=specialists_ids)
                for specialist in selected_specialists:
                    specialist.services.add(service)

            return redirect('reservation:services_list')
        
        specialists = User.objects.filter(role = 'specialist')
        return render(request, 'admin/add_service.html', {'specialists': specialists})

    return redirect('reservation:home')



def edit_service(request, service_id):
    if request.user.is_authenticated and request.user.is_staff:
        service = get_object_or_404(Service, id=service_id)
        specialists= User.objects.filter(role = 'specialist')
        
        if request.method =='POST':
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            price = request.POST.get('price')
            specialists_ids= request.POST.getlist('specialists')

            service.title = title
            service.description = desc
            service.price = price
            service.specialists.set(specialists_ids)
            service.save()
            return redirect('reservation:view_specialists')
        
        return render(request, 'admin/edit_service.html', {'specialists':specialists, 'service':service})
    
    return redirect('reservation:home')





def delete_service(request, service_id):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            service = get_object_or_404(Service, id = service_id)
            service.delete()      
        return redirect('reservation:services_list')
    else:
        return redirect('reservation:home')



def team_view(request):
    specialists = User.objects.filter(role = 'specialist')
    return render(request, 'reservation/our_team.html', {'specialists': specialists})



def view_specialists(request):
    if request.user.is_authenticated:
        specialists = User.objects.filter(role = 'specialist')
        return render(request, 'admin/view_specialists.html', {'specialists': specialists})
    else:
        return redirect('reservation:home')



def add_specialist(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            services_ids = request.POST.getlist('services')

            specialist = User.objects.create(
                username=first_name.lower(),
                first_name = first_name,
                phone = phone,
                email =email,               
                role = 'specialist',
                password = make_password('defaulpassword')            
)   
            selected_services = Service.objects.filter(id__in=services_ids)
            specialist.services.set(selected_services)
            return redirect('reservation:view_specialists')
        
        services = Service.objects.all()
        return render(request, 'admin/add_specialists.html', {'services': services})

    return redirect('reservation:home')



def edit_specialist(request, specialist_id):
    if request.user.is_authenticated and request.user.is_staff:
        specialist=get_object_or_404(User, id=specialist_id, role = 'specialist')
        services = Service.objects.all()
        
        if request.method =='POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            services_ids = request.POST.getlist('services')
            
            specialist.first_name = first_name
            specialist.last_name = last_name
            specialist.phone = phone
            specialist.email = email
            specialist.services.set(services_ids)
            specialist.save()
            return redirect('reservation:view_specialists')
        
        return render(request, 'admin/edit_specialist.html', {'specialist':specialist, 'services':services})

    return redirect('reservation:home')




def delete_specialists(request, number):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            specialists = get_object_or_404(User, id = number, role = 'specialist')
            specialists.delete()     
        return redirect('reservation:view_specialists')
    else:
        return redirect('reservation:home')



def view_clients(request):
    if request.user.is_authenticated:
        clients = User.objects.filter(role = 'client')
        return render(request, 'admin/view_clients.html', {'clients': clients})
    else:
        return redirect('reservation:home')



def add_clients(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            client = User.objects.create(
                username=first_name.lower(),
                first_name = first_name,
                phone = phone,
                email =email,               
                role = 'client',
                password = make_password('defaulpassword')            
)   
            return redirect('reservation:view_clients')
            
        return render(request, 'admin/add_clients.html')
    
    return redirect('reservation:home')




def edit_client(request, client_id):
    if request.user.is_authenticated and request.user.is_staff:
        client=get_object_or_404(User, id=client_id, role = 'client')
        
        if request.method =='POST':
            first_name = request.POST.get('first_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            
            client.first_name = first_name
            client.phone = phone
            client.email = email
            client.save()
            return redirect('reservation:view_clients')
        
        return render(request, 'admin/edit_client.html', {'client':client})

    return redirect('reservation:home')




def delete_client(request, client_id):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            client = get_object_or_404(User, id=client_id, role='client')
            client.delete()
            return redirect('reservation:view_clients') 
    return redirect('reservation:home')





def view_appointments(request):
    if request.user.is_authenticated and request.user.is_staff:
        appointments = []
        selected_specialist=None
        specialists = User.objects.filter(role = 'specialist')
        if request.method == 'POST':
            selected_specialist = request.POST.get('specialist_id')
            if selected_specialist:
                appointments = Booking.objects.filter(specialist__id=selected_specialist).order_by('date', 'time')               
                
        if selected_specialist:
            specialist = User.objects.get(id=selected_specialist)
        else:
            specialist = None
            
        return render(request, 'admin/view_appointments.html', {'appointments': appointments, 'specialists':specialists, 'specialist':specialist ,'selected_specialist':selected_specialist})
    else:
        return redirect('reservation:home')




def choose_service(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            service_id = request.POST.get('service_id')
            if service_id:
                request.session['selected_service']= service_id 
                return redirect('reservation:choose_specialist')
        return redirect('reservation:home')




def choose_specialist(request):
    if not request.user.is_authenticated:
        return redirect('reservation:home')

    service_id = request.session.get('selected_service') 
    if not service_id:
        return redirect('reservation:client_page')


    service = get_object_or_404(Service, id=service_id)
    specialists = User.objects.filter(role='specialist', services=service)

    if request.method == 'POST':
        specialist_id = request.POST.get('specialist_id')
        if specialist_id:
            request.session['selected_specialist'] = specialist_id
            return redirect('reservation:choose_datetime')

    return render(request, 'client/choose_specialist.html', {'service': service, 'specialists': specialists})




def get_available_slot(specialist, date):
    if not specialist.work_start_time or not specialist.work_end_time:
        return []

    booked_times = Booking.objects.filter(specialist=specialist, date=date).values_list('time', flat=True)

    available_times = []
    current_time = datetime.combine(date, specialist.work_start_time)
    end_time = datetime.combine(date, specialist.work_end_time)

    while current_time < end_time:
        if current_time.time() not in booked_times:
            available_times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(hours=1)  # 1 hour slots

    return available_times



def choose_datetime(request):
    if not request.user.is_authenticated:
        return redirect('reservation:home')

    today = datetime.today()
    min_day_value = today.strftime('%Y-%m-%d')

    service_id = request.session.get('selected_service')
    specialist_id = request.session.get('selected_specialist')

    if not service_id or not specialist_id:
        return redirect('reservation:client_page')

    available_times = []
    selected_date = None 
    if request.method == 'POST':
        specialist_id = request.POST.get('specialist_id', specialist_id)  
        specialist = get_object_or_404(User, id=specialist_id, role='specialist')
        selected_date = request.POST.get('date')

        if selected_date:
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            available_times = get_available_slot(specialist, selected_date)

    return render(
        request,
        'client/choose_datetime.html',
        {
            'available_times': available_times,
            'selected_date': selected_date,
            'min_day_value':min_day_value,
        }
    )






def confirm_booking(request):
    if not request.user.is_authenticated:
        return redirect('reservation:home')
    
    if request.method == 'POST':
        specialist_id = request.POST.get('specialist_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        service_id = request.POST.get('service_id')

        if not (specialist_id and service_id and date and time):
            messages.error(request, "Invalid data. Please try again!")
            return redirect('reservation:choose_datetime')

        specialist = get_object_or_404(User, id=specialist_id, role='specialist')
        service = get_object_or_404(Service, id=service_id)

        date = datetime.strptime(date, "%Y-%m-%d").date()
        time = datetime.strptime(time, "%H:%M").time()

        if Booking.objects.filter(specialist=specialist, date=date, time=time).exists():
            messages.error(request, "This time slot is already booked.")
            return redirect('reservation:choose_datetime')

        if request.POST.get('final_confirm') != "true":
            return render(request, 'client/confirm_booking.html', {
                'specialist': specialist,
                'date': date,
                'time': time,
                'service': service
            })


        Booking.objects.create(
            specialist=specialist,
            client=request.user,
            time=time,
            date=date,
            service=service
        )
        return redirect('reservation:booking_success')

    return redirect('reservation:choose_datetime')



def booking_success(request):
    return render(request, 'client/booking_success.html')




def booking_details(request, number):
    if not request.user.is_authenticated:
        return redirect('reservation:home')
    
    booking= get_object_or_404(Booking, id = number)
    booking_datetime = timezone.make_aware(datetime.combine(booking.date, booking.time))

    if booking.service_choices == 'upcoming' and timezone.now() > booking_datetime:
        booking.service_choices = 'completed'
        booking.save()


    if booking.client != request.user:
        return redirect('reservation:home')
    
    if request.method=="POST":
        message_text = request.POST.get('message_text')
        if message_text:
            Message.objects.create(
                booking=booking,
                sender = request.user,
                text=message_text
)        
            messages.success(request, 'Message sent!')
            return redirect('reservation:booking_detail', number=number)
    all_messages = Message.objects.filter(booking=booking).order_by('created_dt')  
    return render(request, 'client/booking_detail.html', {'booking':booking, 'all_messages':all_messages})




def booking_cancel(request, number):
    if not request.user.is_authenticated:
        return redirect('reservation:home')
    
    booking=get_object_or_404(Booking, id=number)
    if booking.client != request.user:
        return redirect('reservation:home')

    booking_datetime = datetime.combine(booking.date, booking.time)
    booking_datetime = timezone.localtime(timezone.make_aware(booking_datetime))
    cancel_deadline = booking_datetime - timedelta(hours=12)
    now_time = timezone.now()

    if now_time > cancel_deadline:
        messages.error(request, "Sorry, but you can't cancel your appointment!" )
        return redirect('reservation:booking_detail', number=number)

    booking.service_choices = 'canceled'
    booking.save()
    
    messages.success(request, "Your appointment has been successfully canceled!")
    return redirect('reservation:booking_detail', number=number)




def client_appointments(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(client = request.user).order_by('date')
        return render(request, 'client/client_appointment.html', {'bookings':bookings})
    else:
        return redirect('reservation:home')
    



def specialist_appointments(request):
    if not request.user.is_authenticated:
        return redirect('reservation:home')
    today = datetime.today()
    min_day_value = today.strftime('%Y-%m-%d')
    selected_date = request.GET.get('date', today.strftime('%Y-%m-%d'))
    bookings = Booking.objects.filter(
        specialist=request.user,
        date=selected_date,       
        ).order_by('time')
    return render(request, 'specialist/specialist_appointment.html', {'bookings':bookings, 'selected_date':selected_date, 'min_day_value':min_day_value})



def delete_appointment(request, appointment_id):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            appointment = get_object_or_404(Booking, id = appointment_id)
            appointment.delete()       
        return redirect('reservation:view_appointments')
    else:
        return redirect('reservation:home')





def specialist_booking_details(request, number):
    if not request.user.is_authenticated:
        return redirect('reservation:home')
    booking= get_object_or_404(Booking, id = number)
    
    if booking.specialist != request.user:
        return redirect('reservation:home')

    if request.method=="POST":
        message_text = request.POST.get('message_text')
        if message_text:
            Message.objects.create(
                booking=booking,
                sender = request.user,
                text=message_text
)        
            messages.success(request, 'Message sent!')
            return redirect('reservation:booking_detail_specialist', number=number)

    all_messages = Message.objects.filter(booking=booking).order_by('created_dt')
    return render(request, 'specialist/booking_detail_for_specialist.html', {'booking':booking, 'all_messages':all_messages})




def view_clients_for_specialist(request):
    if not request.user.is_authenticated:
        return redirect('reservation:home')
    
    clients = Booking.objects.filter(specialist=request.user).values(
        'client__id', 
        'client__first_name', 
        'client__username', 
        'client__phone', 
        'client__email'
    ).distinct()
    return render(request, 'specialist/view_clients_for_specialist.html', {'clients':clients} )






def about(request):
    return render (request, 'reservation/about.html')

def home(request):
    return render (request, 'reservation/home.html')

def contact(request):
    return render (request, 'reservation/contact.html')















# ---------------------------------------MARKS-------------------------------

'''
from django.contrib.auth.decorators import login_required

@login_required(login_url='reservation:home')  # Можно указать свою страницу входа
def client_page(request):
    return render(request, 'client/client_dashboard.html', {'user': request.user})
    
'''