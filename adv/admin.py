from django.contrib import admin
from adv.models import Student, SchoolSubject


class SchoolSubjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student)