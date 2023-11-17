from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('home',views.home1,name='home1'),
    path('addcourse',views.add_course,name='add_course'),
    path('addstu',views.add_stu,name='add_stu'),
    path('showdetails',views.show_details,name='show_details'),
    path('editstu/<int:pid>',views.edit_stu,name='edit_stu'),
    path('editstudetails/<int:pid>',views.edit_stu_details,name='edit_stu_details'),
    path('deletestu/<int:pid>',views.delete_stu,name='delete_stu'),
    path('tcr_view',views.tcr,name='tcr'),
    path('addtcr',views.add_tcr,name='add_tcr'),
    path('log_out',views.logout,name='logout'),
    path('login',views.login1,name='login1'),
    path('about',views.about1,name='about1'),
    path('edittcr',views.edit_tcr,name='edit_tcr'),
    path('edittcrdetails',views.edit_tcr_details,name='edit_tcr_details'),
    path('show_teacher',views.showteacher,name='showteacher'),
    path('showtcr',views.show_tcr,name='show_tcr'),
    path('deletetcr/<int:teacher_id>',views.delete_tcr,name='delete_tcr')
]