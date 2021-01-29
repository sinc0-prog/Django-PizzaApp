# Project Django - SomalPizza WebApp

***
This App is final project in CodersLab School :)

## Inside:

Customer action:

* Register account with activation email
* Register account by social media
* Login/Logout (option reset password with link to add new password)
* Order default pizza (defined by stuff) in 2 sizes.
* Create own pizza with favorites ingredients.
* Update account( delivery address, email, password
* Check orders history
* Check status of order ( confirmed, in production, delivering, delivered, cancelled )
* Payment by PayU 
(Implemented thanks to the original application of our mentor - [https://github.com/cb1986ster/payumoje](https://github.com/cb1986ster/payumoje) 

Stuff action:

* Create and edit pizza for menu.
* Manage toppings
* Check payment status
* Manage status for customer
* Manage users


## To start application locally
* UPDATE DATA IN somalpizza/settings.py
* 


```
$ pip3 install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```



## Other notes

The application is constantly under development.
