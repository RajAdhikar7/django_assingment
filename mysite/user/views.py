
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomUserCreationForm , BlogPostForm ,  AppointmentForm
from .models import PatientProfile, DoctorProfile  , BlogPost  , CustomUser , Appointment 
from django.contrib.auth.decorators import login_required 
from .utils import create_google_calendar_event



def home_view(request):
    return render(request, 'user/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'patient':
                PatientProfile.objects.create(user=user)
            elif user_type == 'doctor':
                DoctorProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def dashboard_view(request):
    user = request.user
    if user.user_type == 'patient':
        return redirect('patient_dashboard')
    elif user.user_type == 'doctor':
        return redirect('doctor_dashboard')
    else:
        return redirect('home')

@login_required
def patient_dashboard_view(request):
    return render(request, 'user/patient_dashboard.html')

@login_required
def doctor_dashboard_view(request):
    return render(request, 'user/doctor_dashboard.html')


@login_required
def create_blog_post_view(request):
    if request.user.user_type != 'doctor':
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('doctor_blog_posts')
    else:
        form = BlogPostForm()
    
    return render(request, 'user/create_blog_post.html', {'form': form})

@login_required
def doctor_blog_posts_view(request):
    if request.user.user_type != 'doctor':
        return redirect('home')
    
    blog_posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'user/doctor_blog_posts.html', {'blog_posts': blog_posts,'doctor_name': request.user.username})

@login_required
def blog_posts_view(request):
    if request.user.user_type != 'patient':
        return redirect('home')
    
    blog_posts = BlogPost.objects.filter(status='published').order_by('-created_at')
    categories = dict(BlogPost.CATEGORY_CHOICES)
    category_dict = {category_key: blog_posts.filter(category=category_key) for category_key, category in categories.items()}
    
    return render(request, 'user/blog_posts.html', {'categories': categories, 'category_dict': category_dict})


@login_required
def doctor_list_view(request):
    doctors = CustomUser.objects.filter(user_type='doctor')
    return render(request, 'user/doctor_list.html', {'doctors': doctors})

@login_required
def book_appointment_view(request, doctor_id):
    doctor = get_object_or_404(CustomUser, pk=doctor_id, user_type='doctor')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()
            create_google_calendar_event(appointment)  # Function to handle Google Calendar API
            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'user/book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def appointment_confirmation_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'user/appointment_confirmation.html', {'appointment': appointment})