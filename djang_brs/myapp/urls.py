from django.urls import path
from . import views

urlpatterns = [
    
    path('newfirst',views.newfirst,name="newfirst"),
    path('hpage',views.hpage,name="hpage"),
    path('', views.first, name="first"),
    path('home',views.home, name="home"),
    path('schedule',views.schedule,name="schedule"),
    path('findbus', views.findbus, name="findbus"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('signup', views.signupPage, name="signup"),
    path('login', views.loginPage, name="login"),
    path('success', views.success, name="success"),
    path('logout', views.logoutPage, name="logout"),
    path('payment',views.payment,name="payment"),
    path('thank',views.thank,name="thank"),
    path('contact',views.contact,name="contact"),
]
