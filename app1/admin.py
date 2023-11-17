from django.contrib import admin
from .models import Course,Student,Usermember

# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Usermember)