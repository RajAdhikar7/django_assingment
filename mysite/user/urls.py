from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup_view, dashboard_view, patient_dashboard_view, doctor_dashboard_view, home_view


urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to 'home' after logout
    path('dashboard/', dashboard_view, name='dashboard'),
    path('patient_dashboard/', patient_dashboard_view, name='patient_dashboard'),
    path('doctor_dashboard/', doctor_dashboard_view, name='doctor_dashboard'),
]