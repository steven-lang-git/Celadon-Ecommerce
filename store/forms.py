from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Order
from django.forms.widgets import TextInput, PasswordInput

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=TextInput(attrs={
        'class': 'ms-input w-input',
        'autofocus': True,
        'placeholder': 'Username or Email'
    }))
    
    password = forms.CharField(widget=PasswordInput(attrs={
        'class': 'ms-input w-input',
        'placeholder': 'Password'
    }))


class RegisterForm(UserCreationForm):
    # email= forms.EmailField()
    username = forms.CharField(max_length=30, widget=TextInput(attrs={
        'class': 'ms-input w-input',
        'autofocus': True,
        'placeholder': 'Username or Email'
    }))

    password1 = forms.CharField(
        label='Enter Password',
        widget=PasswordInput(attrs={
        'class': 'ms-input w-input',
        'placeholder': 'Enter Password'
    }))

    password2 = forms.CharField(
        label='Confirm Password',
        widget=PasswordInput(attrs={
        'class': 'ms-input w-input',
        'placeholder': 'Confirm Password'
    }))
    
    email = forms.EmailField(max_length=200, widget=TextInput(attrs={
        'class': 'ms-input w-input',
        'placeholder': 'Email'
    }))
    class Meta:
        model = User
        fields = ["username", "email","password1","password2"]
     

   
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, widget=TextInput(attrs={
        'class': 'ms-input w-input',
        'placeholder': 'Email'
    }))    
    username = UsernameField(widget=TextInput(attrs={
        'class': 'ms-input w-input',
        'autofocus': True,
        'placeholder': 'Username or Email'
    }))
    class Meta:
        model= User
        fields = ['username', 'email']





class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)



class ShippingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_method']
    SHIPPING_METHODS = [('option1','Standard'),('option2','Express'),('option3','Rush')]
    shipping_method = forms.TypedChoiceField(label='',choices=SHIPPING_METHODS,widget=forms.RadioSelect)

state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class StateForm(forms.Form):
    state_names = [('Alaska', 'AK'), ('Alabama', 'AL'), ('Arkansas', 'AR'), ('Arizona', 'AZ'), ('California', 'CA'), ('Colorado', 'CO'), ('Connecticut', 'CT'), ('District of Columbia', 'DC'), ('Delaware', 'DE'), ('Florida', 'FL'), ('Georgia', 'GA'), ('Hawaii', 'HI'), ('Iowa', 'ID'), ('Idaho', 'IL'), ('Illinois', 'IN'), ('Indiana', 'IA'), ('Kansas', 'KS'), ('Kentucky', 'KY'), ('Louisiana', 'LA'), ('Massachusetts', 'ME'), ('Maryland', 'MD'), ('Maine', 'MA'), ('Michigan', 'MI'), ('Minnesota', 'MN'), ('Missouri', 'MS'), ('Mississippi', 'MO'), ('Montana', 'MT'), ('North Carolina', 'NE'), ('North Dakota', 'NV'), ('Nebraska', 'NH'), ('New Hampshire', 'NJ'), ('New Jersey', 'NM'), ('New Mexico', 'NY'), ('Nevada', 'NC'), ('New York', 'ND'), ('Ohio', 'OH'), ('Oklahoma', 'OK'), ('Oregon', 'OR'), ('Pennsylvania', 'PA'), ('Rhode Island', 'RI'), ('South Carolina', 'SC'), ('South Dakota', 'SD'), ('Tennessee', 'TN'), ('Texas', 'TX'), ('Utah', 'UT'), ('Virginia', 'VT'), ('Vermont', 'VA'), ('Washington', 'WA'), ('Wisconsin', 'WV'), ('West Virginia', 'WI'), ('Wyoming', 'WY')]
    state = forms.ChoiceField(label='', choices = state_names, widget = forms.Select(attrs={ 'class':'form-control','name':'state'}))


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-text',
        'placeholder': 'Enter coupon code'
    }),
    label=False  # Set label to False to remove the label
)    