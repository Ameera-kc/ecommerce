from django import forms
from .models import Login
from django.forms.widgets import TextInput, EmailInput, Textarea
from user.models import Customer
from django.contrib.auth.forms import UserCreationForm


class LoginRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )

    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')

class UserRegistration(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('customer_name', 'phone_number', 'email', 'address')
        widgets= {
            'customer_name': TextInput(attrs={'class':'form-control','name':'customer_name','placeholder':'Full Name','required':'required','autocomplete':'off',}),
            'phone_number':TextInput(attrs={'class':'form-control','name':'phone_number','placeholder':'Phone Number','required':'required','autocomplete':'off',}),
            'email': EmailInput(attrs={'class':'form-control','name':'email','placeholder':'Email','required':'required','autocomplete':'off',}),
            'address':Textarea(attrs={'class':'form-control','name':'address','placeholder':'Full Address','required':'required','autocomplete':'off',}),  
            
       }


# class UserForm(UserCreationForm):
    
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )

#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2')


# class UserForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )
#     class Meta:
#         model = User
#         fields = ('customer_name','phone_number','email','address')
#         widgets= {
#             'customer_name': TextInput(attrs={'class':'form-control','name':'customer_name','placeholder':'Full Name','required':'required','autocomplete':'off',}),
#             'phone_number':TextInput(attrs={'class':'form-control','name':'phone_number','placeholder':'Phone Number','required':'required','autocomplete':'off',}),
#             'email': EmailInput(attrs={'class':'form-control','name':'email','placeholder':'Email','required':'required','autocomplete':'off',}),
#             'address':Textarea(attrs={'class':'form-control','name':'address','placeholder':'Full Address','required':'required','autocomplete':'off',}),  
            
#         }
#         def clean_password2(self):
#             cd = self.cleaned_data
#             if cd['password1'] != ["password2"]:
#                 raise forms.ValidationError("Password dont match")
#             return cd["password2"]

