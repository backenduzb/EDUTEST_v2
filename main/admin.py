from django.contrib import admin
from .models import (
    TestCase,
    Subjects,
    Tests
)


@admin.register(Subjects)
class TestsAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ['name']


@admin.register(TestCase)
class TestsAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_number']
    search_fields = ['title']
    list_filter = ['created_at','class_number']

@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ['correct_answer']
    search_fields = ['question','_case']
    list_filter = ['_case']
