from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from .models import *
from .forms import *
from django.forms.widgets import PasswordInput
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from PizzaApp.tokens import account_activation_token
from django.forms import CheckboxSelectMultiple
import json


# View homepage app

class Home(View):
    def get(self, request):
        messages.info(
            request, f"Welcome we are using cookies. By closing this alert you'll agree for that. Enjoy :)")
        return render(request, 'base.html')


# Login user view

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login_user.html'
    success_url = '/dashboard'

    def get(self, request):
        if request.user.is_authenticated:
            messages.success(request, f"Welcome again {request.user}!")
            return render(request, 'dashboard.html')
        else:
            return super(LoginView, self).get(request)

    def form_valid(self, form):
        user = form.authenticate_user()
        try:
            login(self.request, user)
            messages.success(self.request, f"Welcome again {user}!")
            return redirect('dashboard')
        except Exception:
            messages.error(
                self.request, "Login process failed! Click 'Forgot the passord?' or register now!")
            return redirect('/login/')


# View to logout user

class LogOutUser(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            logout(request)
            messages.success(request, "You are logged out now! GoodBye!")
        return redirect('/home/')


# View to dashboard after login

class DashView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = self.request.user
        user_data = CustomClient.objects.get(id=user.id)
        if user_data.city == None or user_data.email == "":
            messages.warning(
                request, 'Your account is not complate. Please update all data')
            return redirect('update-user')
        elif len(user_data.password) < 78:
            messages.warning(
                request, 'You signed up by socialmedia. Required update account and password data.')
            return redirect('change-password')

        pizza_list = Pizza.objects.filter(is_special=True, size=40)
        form = ChooseSizePizza
        return render(request, 'dashboard.html', {'pizza_list': pizza_list, 'form': form, "user": user})


# View to define pizza

class CreatePizza(SuccessMessageMixin, CreateView):
    form_class = CreatePizza
    template_name = 'create_pizza.html'
    success_url = '/staff_pizza_list/'
    success_message = "Created success!"


# View to add toppings

class AddToppingView(SuccessMessageMixin, CreateView):
    form_class = AddToppingsForm
    template_name = 'add_toppings.html'
    success_url = '/toppings/'
    success_message = "Added success!"


# View shows defined pizzas

class PizzaList(View):

    def get(self, request):
        if request.user.is_authenticated:
            pizza_list = Pizza.objects.filter(is_special=False, size=40)
            form = ChooseSizePizza
            return render(request, 'menu.html', {'pizza_list': pizza_list, 'form': form})
        else:
            messages.warning(
                request, "Our delicious pizzas only for trusted!  Let's check our pizzas and signin for add to cart :)")
            pizza_list = Pizza.objects.filter(is_special=False, size=40)
            form = ChooseSizePizza
            return render(request, 'menu.html', {'pizza_list': pizza_list, 'form': form})


# User View

class UserView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user_id = request.user.id
        user_obj = CustomClient.objects.filter(pk=user_id)
        return render(request, 'account.html', {'user_obj': user_obj,
                                                'user_id': user_id})


# Change password for User

class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_url = '/dashboard/'
    login_url = '/login/'
    success_message = "Password updated succesfull!"

    def get_user(self):
        user_id = self.request.user.id
        user = CustomClient.objects.get(id=user_id)
        return user

    def form_valid(self, form):
        user = self.get_user()
        new_password = form.cleaned_data['password']
        user.set_password(new_password)
        user.save()
        return super(ChangePasswordView, self).form_valid(form)


# Update User data (without password/username)

class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = UpdateUser
    template_name = 'update_account_data.html'
    success_url = '/dashboard/account'
    login_url = '/login/'
    success_message = "Account updated succesfull!"

    def get_initial(self):
        user_id = self.request.user.id
        user_obj = CustomClient.objects.get(id=user_id)
        return {'first_name': user_obj.first_name,
                'last_name': user_obj.last_name,
                'email': user_obj.email,
                'city': user_obj.city,
                'post_code': user_obj.post_code,
                'street': user_obj.street,
                'number_of_builing': user_obj.number_of_builing,
                'flat_number': user_obj.flat_number,
                'phone_number': user_obj.phone_number}

    def get_user(self):
        user_id = self.request.user.id
        user = CustomClient.objects.get(id=user_id)
        return user

    def form_valid(self, form):
        user = self.get_user()
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.city = form.cleaned_data['city']
        user.post_code = form.cleaned_data['post_code']
        user.street = form.cleaned_data['street']
        user.number_of_builing = form.cleaned_data['number_of_builing']
        user.flat_number = form.cleaned_data['flat_number']
        user.phone_number = form.cleaned_data['phone_number']
        user.save()
        return super(UpdateUser, self).form_valid(form)


# Cart View

class CartView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        client = request.user
        order, created = Orders.objects.get_or_create(
            client=client, order_status='IN CART')
        items = order.itemorder_set.all().order_by('id')
        ctx = {'items': items, 'order': order}
        return render(request, 'cart.html', ctx)


# Update User Adress

class UpdateUserAdress(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = UpdateUserAdressForm
    template_name = 'update_adress.html'
    success_url = '/dashboard/'
    login_url = '/login/'
    success_message = "Account updated succesfull!"

    def get_user(self):
        user_id = self.request.user.id
        user = CustomClient.objects.get(id=user_id)
        return user

    def form_valid(self, form):
        user = self.get_user()
        user.city = form.cleaned_data['city']
        user.post_code = form.cleaned_data['post_code']
        user.street = form.cleaned_data['street']
        user.number_of_builing = form.cleaned_data['number_of_builing']
        user.flat_number = form.cleaned_data['flat_number']
        user.phone_number = form.cleaned_data['phone_number']
        user.save()
        return super(UpdateUserAdress, self).form_valid(form)


# Cart Checkout View

class CartCheckoutView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        client = request.user
        order, created = Orders.objects.get_or_create(
            client=client, order_status='IN CART')
        items = order.itemorder_set.all()
        ctx = {'items': items, 'order': order}
        return render(request, 'Checkout.html', ctx)


# Update Item in Cart

class UpdateItem(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        size = data['size']
        pizza_name = data['pizza_name']
        print('productId:', productId, 'action:',
              action, 'name', pizza_name, 'size:', size)
        user = request.user
        is_exist = Pizza.objects.filter(name=pizza_name, size=size)
        if is_exist.count() == 1:
            product = Pizza.objects.get(name=pizza_name, size=size)
            product.price = product.get_my_price
            order, created = Orders.objects.get_or_create(
                client=user, order_status='IN CART')
            itemorder, created = ItemOrder.objects.get_or_create(
                order=order, product=product)

            if action == 'add':
                itemorder.quantity += 1
                messages.success(
                    request, f"Added {product.name} size: {product.size}cm  x  {itemorder.quantity} ")
            elif action == 'remove':
                itemorder.quantity -= 1

            itemorder.save()

            if itemorder.quantity <= 0:
                itemorder.delete()

            return JsonResponse({'data': 'Item was added'}, safe=False)

        else:
            product_base = Pizza.objects.get(id=productId)
            toppings_base = product_base.toppings.all()
            new_product = Pizza.objects.create(name=pizza_name, size=size)
            new_product.toppings.set(toppings_base)
            new_product.price = new_product.get_my_price
            new_product.save()
            order, created = Orders.objects.get_or_create(
                client=user, order_status='IN CART')
            itemorder, created = ItemOrder.objects.get_or_create(
                order=order, product=new_product, price=new_product.price)

            if action == 'add':
                itemorder.quantity += 1
                messages.success(
                    request, f"Added {new_product.name} size: {new_product.size}cm  x  {itemorder.quantity} ")
            elif action == 'remove':
                itemorder.quantity -= 1

            itemorder.save()

            if itemorder.quantity <= 0:
                itemorder.delete()

            return JsonResponse({'data': 'Item was added'}, safe=False)


# Create Special View

class CreateSpecial(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = CreateSpecialForm
        return render(request, 'create_special.html', {'form': form})

    def post(self, request):
        form = CreateSpecialForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            toppings = form.cleaned_data['toppings']
            size = form.cleaned_data['size']
            add_cheese = form.cleaned_data['add_cheese']
            spec_pizza = Pizza.objects.create(
                name=name, size=size, add_cheese=add_cheese, is_special=True)
            spec_pizza.toppings.set(toppings)
            spec_pizza.price = spec_pizza.get_my_price
            spec_pizza.save()
            order, created = Orders.objects.get_or_create(
                client=request.user, order_status='IN CART')
            itemorder, created = ItemOrder.objects.get_or_create(
                order=order, quantity=1, product=spec_pizza, price=spec_pizza.price)
            messages.success(
                request, f"Added {spec_pizza.name} size: {spec_pizza.size}cm  x  {itemorder.quantity} ")
            return render(request, 'create_special.html', {'form': form, 'spec_pizza': spec_pizza})
        form = CreateSpecialForm
        messages.error(request, f"Something went wrong. Try again!")
        return render(request, 'create_special.html', {'form': form})


# User order list

class OrderList(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = request.user
        orders = Orders.objects.filter(client=user).exclude(order_status = 'IN CART').order_by('-order_time')
        return render(request, 'orders_list.html', {'user': user, 'orders': orders})


# Staff Panel Pizza View

class PizzaListAdmin(View):

    def get(self, request):
        pizza_list = Pizza.objects.filter(is_special=False, size=40)
        return render(request, 'admin_pizza_list.html', {'pizza_list': pizza_list})


# Staff panel toppings view

class ToppingsListAdmin(View):

    def get(self, request):
        toppings_list = Toppings.objects.filter()
        return render(request, 'admin_toppings_list.html', {'toppings_list': toppings_list})


# Staff panel order list

class OrderListAdmin(View):

    def get(self, request):
        orders = Orders.objects.exclude(
            order_status="DELIVERED").exclude(order_status ="IN CART").order_by('-order_time')
        form = ChooseStatus()
        return render(request, 'order_list_admin.html', {'orders': orders, 'form': form})

    def post(self, request):
        form = ChooseStatus(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            order_id = request.POST.get("order_id")
            _order = Orders.objects.get(id=order_id)
            _order.order_status = status
            _order.save()
            messages.success(
                request, f"The order no. {order_id} --- STATUS changed for {status} !")
            orders = Orders.objects.exclude(
                order_status="DELIVERED").order_by('-order_time')
            return render(request, 'order_list_admin.html', {'orders': orders, 'form': form})
        messages.error(request, f"Something went wrong. Try again!")
        return render(request, 'order_list_admin.html', {'orders': orders, 'form': form})


# Staff panel update pizza

class UpdatePizza(SuccessMessageMixin, UpdateView):
    model = Pizza
    fields = '__all__'
    widgets = {
        'toppings': CheckboxSelectMultiple()}
    template_name = 'create_pizza.html'
    success_message = "Update success!"

    def get_success_url(self):
        return str(reverse_lazy('staff_pizza_list'))


# Staff panel - delete topping

class DeleteTopping(SuccessMessageMixin, DeleteView):
    model = Toppings
    template_name = 'delete_topping_confirm.html'
    success_message = "Delete success!"

    def get_success_url(self):
        return str(reverse_lazy('toppings_list'))


# Staff panel - delete pizza

class DeletePizza(DeleteView, SuccessMessageMixin):
    model = Pizza
    template_name = 'delete_pizza_confirm.html'
    success_message = "Delete success!"

    def get_success_url(self):
        return str(reverse_lazy('staff_pizza_list'))


# SignUp View

class SignUpView(View):

    def get(self, request):
        form = SignUpForm
        return render(request, 'register_form.html', {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            is_exist = CustomClient.objects.filter(email=email)
            if is_exist.count() > 0:
                form = SignUpForm()
                messages.error(request, "Sorry! You are already registered!")
                return render(request, 'register_form.html', {'form': form})
            user = CustomClient.objects.create(first_name=first_name, last_name=last_name,
                                               username=username, email=email, is_active=False)
            user.set_password(password)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your pizza account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(
                request, "Please confirm your email address to complete the registration")
            return redirect('/login/')
        else:
            form = SignUpForm()
            messages.error(request, "Sorry! Something went wrong. Try Again! Type all fields")
            return render(request, 'register_form.html', {'form': form})


# Activate user account

class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomClient._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomClient.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, "Thank you for your email confirmation. Now you can login your account.")
            return redirect('/login/')
        else:
            messages.error(request, "Activation link is invalid!")
            return redirect('/home/')
