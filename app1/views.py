from django.shortcuts import render,redirect
from .models import Course,Student,Usermember
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
import os

def loginpage(req):
    if req.user.is_authenticated:
        if req.user.is_staff:
            return redirect('home1')
        else:
            return redirect('about1')
    return render(req, 'login.html')

@login_required(login_url='loginpage')
def home1(req):
    if not req.user.is_superuser:
        return redirect('about1')
    courses = Course.objects.all()
    return render(req, 'homepage.html', {'course': courses, 'user': req.user})

@login_required(login_url='loginpage')
def about1(req):
    if req.user.is_superuser:
        return redirect('home1')
    welcome_message = req.session.get('welcome_message')
    return render(req, 'about.html', {'welcome_message': welcome_message})

@login_required(login_url='loginpage')
def add_course(req):
    if req.method=='POST':
        course_name=req.POST['course1']
        course_fee=req.POST['fee1']
        course=Course(course_name=course_name,fee=course_fee)
        course.save()
        return redirect('home1')

@login_required(login_url='loginpage')
def add_stu(req):
    if req.method=='POST':
        student_name=req.POST['stuname']
        student_email=req.POST['stuemail']
        student_age=req.POST['stuage']
        j_date=req.POST['studate']
        sel=req.POST['sel']
        course=Course.objects.get(id=sel)
        student=Student(course=course,student_name=student_name,e_address=student_email,student_age=student_age,joining_date=j_date)
        student.save()
        return redirect('show_details')

@login_required(login_url='loginpage')
def show_details(req):
    if not req.user.is_superuser:
        return redirect('about1')
    student=Student.objects.all()
    return render(req,'studentdetails.html',{'stu':student})

@login_required(login_url='loginpage')
def edit_stu(req,pid):
    if not req.user.is_superuser:
        return redirect('about1')
    student=Student.objects.get(id=pid)
    course=Course.objects.all()
    return render(req,'editstudent.html',{'student':student,'course':course})

@login_required(login_url='loginpage')
def edit_stu_details(req,pid):
    if req.method=='POST':
        student=Student.objects.get(id=pid)
        student.student_name=req.POST['sname']
        student.e_address=req.POST['semail']
        student.student_age=req.POST['sage']
        student.joining_date=req.POST['sdate']
        sel=req.POST['scourse']
        course=Course.objects.get(id=sel)
        student.course=course
        student.save()
        return redirect('show_details')
    return render(req,'editstudent.html')

@login_required(login_url='loginpage')
def delete_stu(req,pid):
    if not req.user.is_superuser:
        return redirect('about1')
    student=Student.objects.get(id=pid)
    student.delete()
    return redirect('show_details')

def tcr(req):
    courses=Course.objects.all()
    return render(req,'addteacher.html',{'course':courses})

def add_tcr(req):
    if req.method=='POST':
        fn=req.POST['tfname']
        ln=req.POST['tlname']
        uname=req.POST['tusername']
        em=req.POST['temail']
        ph=req.POST['tphone']
        ag=req.POST['tage']
        add=req.POST['taddress']
        image=req.FILES.get('img1')
        pass1=req.POST['pwd1']
        pass2=req.POST['pwd2']
        sel=req.POST['sel']
        course=Course.objects.get(id=sel)
        if pass1==pass2:
            if User.objects.filter(username=uname).exists():
                messages.info(req,'This username already exists!!!')
                return redirect('tcr')
            else:
                user=User.objects.create_user(
                    first_name=fn,
                    last_name=ln,
                    username=uname,
                    password=pass1,
                    email=em)
                user.save()
                usmem=Usermember(course=course,user=user,address=add,age=ag,phone_number=ph,image=image)
                usmem.save()
        else:
            messages.info(req,'Password not mathing!!! Try Again...')
            return redirect('tcr')
        return redirect('loginpage')
    else:
        return render(req,'login.html')

def login1(req):
    if req.method == 'POST':
        username1 = req.POST['usrname']
        password1 = req.POST['pwd']
        user = auth.authenticate(username=username1, password=password1)
        if user is not None:
            if user.is_superuser:
                login(req, user)
                return redirect('home1')
            else:
                login(req, user)
                req.session['welcome_message'] = f'Welcome {username1}'
                return redirect('about1')
        else:
            messages.info(req, 'Invalid username or password! Try Again...')
            return redirect('loginpage')
    else:
        return redirect('loginpage')


@login_required(login_url='loginpage')
def logout(req):
    auth.logout(req)
    return redirect('loginpage')

@login_required(login_url='loginpage')
def edit_tcr(req):
    user=req.user.id
    teacher=Usermember.objects.get(user=user)
    course=Course.objects.all()
    return render(req,'editteacher.html',{'teacher':teacher,'course':course})

@login_required(login_url='loginpage')
def edit_tcr_details(req):
    if req.method=='POST':
        user=User.objects.get(id=req.user.id)
        teacher=Usermember.objects.get(user_id=req.user.id)
        user.first_name=req.POST['tfname']
        user.last_name=req.POST['tlname']
        user.username=req.POST['tusrname']
        user.email=req.POST['temail']
        teacher.age=req.POST['tage']
        teacher.phone_number=req.POST['tphone']
        if len(req.FILES)!=0:
            if len(teacher.image)>0:
                os.remove(teacher.image.path)
            teacher.image=req.FILES.get('imgfile')
        teacher.address=req.POST['taddress']
        sel=req.POST['scourse']
        course=Course.objects.get(id=sel)
        teacher.course=course
        teacher.save()
        user.save()
        return redirect('showteacher')
    return render(req,'editteacher.html')

@login_required(login_url='loginpage')
def showteacher(req):
    user=req.user.id
    teacher=Usermember.objects.get(user=user)
    course=Course.objects.all()
    return render(req,'teacherprofile.html',{'teacher':teacher,'course':course})

@login_required(login_url='loginpage')
def show_tcr(req):
    teacher=Usermember.objects.all()
    return render(req,'teacherdetails.html',{'tcr':teacher})

@login_required(login_url='loginpage')
def delete_tcr(req, teacher_id):
    teacher = get_object_or_404(Usermember, id=teacher_id)
    user = User.objects.get(id=teacher.user.id)
    teacher.delete()
    user.delete()
    return redirect('show_tcr')
