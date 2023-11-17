from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    course_name=models.CharField(max_length=255)
    fee=models.IntegerField()

    def __str__(self):
        return self.course_name

class Student(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    student_name=models.CharField(max_length=255)
    e_address=models.EmailField()
    student_age=models.IntegerField()
    joining_date=models.DateField()

    def __str__(self):
        return self.student_name

class Usermember(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255)
    age=models.IntegerField()
    phone_number=models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='image/',null=True)