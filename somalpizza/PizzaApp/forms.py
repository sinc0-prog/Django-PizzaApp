from .models import *
from django.forms import PasswordInput, ModelForm
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .validators import *


# SignUp Form
class SignUpForm(ModelForm):
    repeat_password = forms.CharField(
        max_length=254, widget=forms.PasswordInput)


    class Meta:
        model = CustomClient
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password', 'repeat_password']
        widgets = {
            'password': PasswordInput()}
        help_texts = {
            'username': None,
        }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data['password']
        repeat_password = cleaned_data['repeat_password']
        email = cleaned_data['email']
        username = cleaned_data['username']
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        if first_name == "" or last_name == "":
            raise ValidationError('First name and last name are required!')
        if password != repeat_password:
            raise ValidationError('Passwords are not same!')
        elif len(password)< 8:
            raise ValidationError('Password should more than 8!')
        return cleaned_data


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(max_length=254, widget=forms.PasswordInput())

    def authenticate_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        return user

# Staff create new pizza


class CreatePizza(ModelForm):
    toppings = forms.ModelMultipleChoiceField(
        queryset=Toppings.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = forms.ChoiceField(choices=SIZE_PIZZA, widget=forms.Select)
    add_cheese = forms.ChoiceField(
        choices=((False, 'No'), (True, 'Yes')), widget=forms.Select)

    class Meta:
        model = Pizza
        fields = '__all__'

# Staff add topping


class AddToppingsForm(ModelForm):
    class Meta:
        model = Toppings
        fields = '__all__'

# Staff Update Status Order


class ChooseStatus(forms.Form):
    status = forms.ChoiceField(
        choices=ORDER_STATUS, widget=forms.Select, label=False, help_text=None)

# User change password


class PasswordChangeForm(ModelForm):
    repeat_password = forms.CharField(
        max_length=254, widget=forms.PasswordInput)

    class Meta:
        model = CustomClient
        fields = [
            'password', 'repeat_password']
        widgets = {
            'password': PasswordInput(),
            'repeat_passwrod': PasswordInput()}

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password = cleaned_data['password']
        repeat_password = cleaned_data['repeat_password']
        if password != repeat_password:
            raise ValidationError('Passwords are not same!')
        return cleaned_data

# User choose size pizza


class ChooseSizePizza(ModelForm):
    size = forms.ChoiceField(
        choices=SIZE_PIZZA, widget=forms.RadioSelect, label=False, help_text=None)

    class Meta:
        model = Pizza
        fields = ['size']

# User Create Special Pizza


class CreateSpecialForm(ModelForm):
    name = forms.CharField(max_length= 32, validators= [valid_pizza_name])
    toppings = forms.ModelMultipleChoiceField(
        queryset=Toppings.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = forms.ChoiceField(choices=SIZE_PIZZA, widget=forms.Select)
    add_cheese = forms.ChoiceField(
        choices=((False, 'No'), (True, 'Yes')), widget=forms.Select)

    class Meta:
        model = Pizza
        fields = ['name', 'toppings', 'size', 'add_cheese']



# Update User adress data
class UpdateUserAdressForm(ModelForm):
    class Meta:
        model = CustomClient
        fields = [
            'city', 'post_code',
            'street', 'number_of_builing', 'flat_number', 'phone_number']

# Update User Data


class UpdateUser(ModelForm):
    class Meta:
        model = CustomClient
        fields = [
            'first_name', 'last_name',
            'email', 'city', 'post_code',
            'street', 'number_of_builing', 'flat_number', 'phone_number']
