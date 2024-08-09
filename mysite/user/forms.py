from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser , BlogPost , Appointment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'profile_picture', 'username', 'email', 'password1', 'password2', 'address', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Customizing field labels or widgets
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        

        
        if password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        
       
        
        return cleaned_data


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'status']

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['summary'].widget = forms.Textarea(attrs={'rows': 2})
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 10})  

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['speciality', 'date', 'start_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.SelectDateWidget()
        self.fields['start_time'].widget = forms.TimeInput(format='%H:%M', attrs={'type': 'time'})

