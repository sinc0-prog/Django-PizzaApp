"""somalpizza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from PizzaApp.views import *
from django.views.generic.base import TemplateView
from PizzaApp.views import *
from django.contrib.auth import views as auth_views
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    # Staff Url's
    path('admin/', admin.site.urls),
    path('staff_pizza_list/', staff_member_required(PizzaListAdmin.as_view()),
         name='staff_pizza_list'),
    path('toppings/', staff_member_required(ToppingsListAdmin.as_view()),
         name='toppings_list'),
    path('add_pizza/', staff_member_required(CreatePizza.as_view()), name='add_pizza'),
    path('add_topping', staff_member_required(
        AddToppingView.as_view()), name='add-topping'),
    path('add_pizza/', staff_member_required(CreatePizza.as_view()), name='add_pizza'),
    path('orders', staff_member_required(
        OrderListAdmin.as_view()), name='staff_order_list'),
    path('update_pizza/<int:pk>',
         staff_member_required(UpdatePizza.as_view()), name='update_pizza'),
    path('delete_topping/<int:pk>',
         staff_member_required(DeleteTopping.as_view()), name='delete_topping'),
    path('delete_pizza/<int:pk>',
         staff_member_required(DeletePizza.as_view()), name='delete_pizza'),

    path('home/', Home.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout_user/', LogOutUser.as_view(), name="logout-user"),
    path('dashboard/', DashView.as_view(), name='dashboard'),
    path('create_special/', CreateSpecial.as_view(), name='create-special'),

    # Dashboard URL's
    path('dashboard/menu', PizzaList.as_view(), name='pizza_list_public'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/confirm', CartCheckoutView.as_view(), name='confirm_cart'),

    # Account URL's
    path('orders/', OrderList.as_view(), name='orders_list'),
    path('dashboard/account/', UserView.as_view(), name='user-view'),
    path('dashboard/account/change_password/',
         ChangePasswordView.as_view(), name='change-password'),
    path('dashboard/account/update/', UpdateUser.as_view(), name='update-user'),
    path('dashboard/account/update_adress',
         UpdateUserAdress.as_view(), name='update-adress'),

    # Reset password Url's
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_send.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
         name='password_reset_complete'),
    path('update_item/', UpdateItem.as_view(), name='update_item'),
    # path Social Auth
    path('oauth/', include('social_django.urls', namespace='social')),
    # SignUp urls
    path('activate/<uidb64>/<token>/',
         ActivateAccount.as_view(), name='activate'),
    path('signup/', SignUpView.as_view(), name='signup'),
    # path PayU
    path("", include("PayU.urls")),
]
