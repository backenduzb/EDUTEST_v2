from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Schools

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'is_staff', 'is_active','is_teacher','is_student']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_teacher','is_student','region','city','class_letter','class_number','school_token','info_token','students_token','class_raiting','student_raiting')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_teacher','is_student','region','city','class_letter','class_number','school_token','info_token','students_token','class_raiting','student_raiting')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Schools)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['school_name','region','city','teachers_token']
    list_filter = ['region','city']
    search_fields = ['school_name','region','city','teachers_token']