from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from reservation import models


admin.site.register(models.Service)
admin.site.register(models.Booking)
admin.site.register(models.Message)


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone','work_start_time', 'work_end_time', 'services' )}),  # Добавляем в редактирование
    )

    list_display = ('username', 'first_name', 'role', 'is_staff')  # Отображение в списке пользователей
    list_filter = ('role',)  # Фильтр по ролям
    search_fields = ('username', 'first_name', 'last_name')  # Поиск
    filter_horizontal = ('services',)  # Красивый выбор услуг в админке
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Преобразуем в список, чтобы можно было изменять
        fieldsets = list(fieldsets)
        # Если редактируем уже существующего пользователя и он не специалист,
        # убираем поле 'services' из дополнительного набора полей
        if obj and obj.role == 'client':
            new_fieldsets = []
            for title, options in fieldsets:
                if 'fields' in options:
                    # Фильтруем поля, исключая 'services'
                    new_fields = tuple(f for f in options['fields'] if f not in ('services', 'work_start_time', 'work_end_time'))
                    new_options = options.copy()
                    new_options['fields'] = new_fields
                    new_fieldsets.append((title, new_options))
                else:
                    new_fieldsets.append((title, options))
            fieldsets = tuple(new_fieldsets)
        return fieldsets

 


# -----------------------------------------------
#  # Добавляем is_specialist в панель редактирования пользователя
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('is_specialist', 'services')}),  # Поля, которые можно редактировать
#     )

#     # Отображаем is_specialist в списке пользователей
#     list_display = ('username', 'first_name', 'second_name', 'is_specialist', 'is_staff')
    
#     # Фильтр в админке по специалистам
#     list_filter = ('is_specialist',)
    
#     # Поиск в админке
#     search_fields = ('username', 'first_name', 'second_name')
 



admin.site.register(User, CustomUserAdmin)





































#!!! Написать в начале после импортов
# Register your models here.


# from django.contrib import admin
# from . import models

# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'price')  # Поля для отображения в списке

# class SpecialistAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'second_name', 'specialization') #если специализация ForeignKey
#     #list_display = ('first_name', 'second_name') #если специализация ManyToManyField

# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'specialist', 'date', 'time')  # Отображаемые поля
#     list_filter = ('date', 'specialist') # Фильтры справа

# admin.site.register(models.Service, ServiceAdmin)
# admin.site.register(models.Specialist, SpecialistAdmin)
# admin.site.register(models.Appointment, AppointmentAdmin)
