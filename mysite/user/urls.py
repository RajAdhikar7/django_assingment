from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    signup_view, dashboard_view, patient_dashboard_view, 
    doctor_dashboard_view, home_view, create_blog_post_view,
    doctor_blog_posts_view, blog_posts_view ,  doctor_list_view, 
    book_appointment_view , appointment_confirmation_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to 'home' after logout
    path('dashboard/', dashboard_view, name='dashboard'),
    path('patient_dashboard/', patient_dashboard_view, name='patient_dashboard'),
    path('doctor_dashboard/', doctor_dashboard_view, name='doctor_dashboard'),
    path('create_blog_post/', create_blog_post_view, name='create_blog_post'),
    path('doctor_blog_posts/', doctor_blog_posts_view, name='doctor_blog_posts'),
    path('blog_posts/', blog_posts_view, name='blog_posts'),
    path('doctors/', doctor_list_view, name='doctor_list'),
    path('book_appointment/<int:doctor_id>/', book_appointment_view, name='book_appointment'),
    path('appointment_confirmation/<int:appointment_id>/', appointment_confirmation_view, name='appointment_confirmation'),
]
