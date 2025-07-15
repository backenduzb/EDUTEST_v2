from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Schools, generate_username


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'is_staff', 'is_active', 'is_teacher', 'is_student','see_password']
    search_fields = ['is_teacher','is_student']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_teacher', 'is_student',
                'region', 'city',
                'class_letter', 'class_number',
                'school_token', 'info_token', 'students_token',
                'class_raiting', 'student_raiting'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name', 'last_name',
                'username', 'password1', 'password2',
                'is_active', 'is_staff', 'is_superuser',
                'is_teacher', 'is_student',
                'region', 'city',
                'class_letter', 'class_number',
                'school_token', 'info_token', 'students_token',
                'class_raiting', 'student_raiting'
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            if not obj.username:
                obj.username = generate_username(obj.first_name or 'user', obj.last_name or 'name')

            password = form.cleaned_data.get('password1')
            if password:
                messages.success(request, f"Foydalanuvchining paroli: {password}")

        super().save_model(request, obj, form, change)

@admin.register(Schools)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['school_name','region','city','teachers_token']
    list_filter = ['region','city']
    search_fields = ['school_name','region','city','teachers_token']