from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book, Registration,Contact,Refund
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

import razorpay
from myproject.settings import RAZOPAY_API_KEY, RAZOPAY_API_SECRET_KEY
from django.urls import reverse

def first(request):
    return redirect('hpage')

def hpage(request):
    return render(request,'myapp/homepage.html')

def newfirst(request):
    return render(request,'myapp/first.html')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/homepage.html')
    else:
        return render(request, 'myapp/signup.html')

def contact(request):
    return render(request,'myapp/contact.html')



def findbus(request):
    dicti = {}
    context = {}
    data = Bus.objects.all().order_by('date','time')
    dicti = {
        'data': data
    }
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        date_r = datetime.strptime(date_r,"%Y-%m-%d").date()
        year = date_r.strftime("%Y")
        month = date_r.strftime("%m")
        day = date_r.strftime("%d")
        
        # date_r = datetime.strptime(date_r, "%Y-%m-%d").date()
        # today = datetime.now().date()
        # day_difference = (date_r - today).days
        
        # if day_difference > 15:
        #     context["error"] = "Selected date is more than 15 days in the past. Please select a valid date."
        #     return render(request,'myapp/findbus.html',context)


        # create session data
        request.session['payment_data'] = {
           'source_r': source_r,
           'destination_r': dest_r,
           'year':year,
           'month':month,
           'day':day,
           
        }

            
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date__year=year, date__month=month, date__day=day)
        dicti = {'bus_list' : bus_list}
        if bus_list:
            return render(request, 'myapp/list.html', dicti)
        else:
            context = {
                'data':data,
               'error':"No available Bus Schedule for entered Route and Date"
            }
            # context['data'] = request.POST
            # context["error"] = "No available Bus Schedule for entered Route and Date"
            return render(request, 'myapp/findbus.html', context)

    # Retrieve source and destination data from the Bus model
    source_data = Bus.objects.values_list('source', flat=True).distinct()
    destination_data = Bus.objects.values_list('dest', flat=True).distinct()

    context = {
        'source_data': source_data,
        'destination_data': destination_data,
        'data': data
    }

    return render(request, 'myapp/findbus.html', context)


def schedule(request):
    data = Bus.objects.all()
    dicti = {
        'data': data
    }
    return render(request,'myapp/schedule.html',dicti)


@login_required(login_url='newfirst')
@csrf_exempt
def bookings(request):
    context = {}
    dicti = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = request.POST.get('no_seats')
        # bus1 = Bus.objects.all()
        bus = Bus.objects.get(id=id_r)
        print(id_r)
        # print(bus1)
        if bus.rem >= int(seats_r) and bus.rem>0:
        
           # create session data
           request.session['booking_data'] = {
            'id_r': id_r,
            'seats_r': seats_r,
           }
           return redirect('payment')
               
        else:
            if bus.rem == 0:
                payment_data = request.session.get('payment_data',{})
                source_r = payment_data.get('source_r')
                dest_r = payment_data.get('destination_r')
                year = payment_data.get('year')
                month = payment_data.get('month')
                day = payment_data.get('day')

                bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date__year=year, date__month=month, date__day=day)
                context = {'bus_list' : bus_list,
                        'error' : "No Seats Remaining",}
            
                return render(request, 'myapp/list.html', context)
            
            else:
            
                payment_data = request.session.get('payment_data',{})
                source_r = payment_data.get('source_r')
                dest_r = payment_data.get('destination_r')
                year = payment_data.get('year')
                month = payment_data.get('month')
                day = payment_data.get('day')

                bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date__year=year, date__month=month, date__day=day)
                context = {'bus_list' : bus_list,
                        'error' : "Sorry select fewer number of seats",}

            
                return render(request, 'myapp/list.html', context)


    # return render(request,'myapp/bookings.html')

@login_required(login_url='newfirst')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            
            
            if book.status=='CANCELLED':
                messages.success(request, "Your Booking Is Already Cancelled.")
            
            else:
                rem_r = bus.rem + book.nos
                Bus.objects.filter(id=book.busid).update(rem=rem_r)
                #nos_r = book.nos - seats_r

                username = book.name
                busname = book.bus_name
                source = book.source
                destination = book.dest
                nofseats = book.nos
                price = bus.price
                date = book.date
                time = book.time
                refundprice = int(int(nofseats) * int(price))

                en = Refund(username=username,busname=busname,source=source,destination=destination,
                nofseats=nofseats,price=price,date=date,time=time,refundprice=refundprice)
                en.save()

                Book.objects.filter(id=id_r).update(status='CANCELLED')
                Book.objects.filter(id=id_r).update(nos=0)
                messages.success(request, "Booked Bus has been cancelled successfully.")

            return redirect(seebookings)

        except Book.DoesNotExist:
            context["error"] = "Sorry You Have Not Booked That Bus"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='newfirst')
def seebookings(request):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)

    if book_list:
        return render(request, 'myapp/booklist.html', {'book_list': book_list})
    else:
        context["error"] = "Sorry, no buses booked"
        return render(request, 'myapp/findbus.html', context)

@login_required(login_url='newfirst')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        message = request.POST.get('Message')

        en = Contact(name=name,email=email,message=message)
        en.save()

    return render(request,'myapp/contact.html')

def signupPage(request):
    if request.method=='POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if(pass1!=pass2):
            return HttpResponse('Password Not Matched')
        else:
            my_user=User.objects.create_user(name,email,pass1)
            my_user.save() 
           
            return redirect('login')

    return render(request,'myapp/signup.html')

def loginPage(request):
    if request.method == "POST":
        username=request.POST.get('username')
        pass1 = request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password Incorrect")

    return render(request,'myapp/login.html')

def logoutPage(request):
    logout(request)
    return redirect('newfirst')
           



def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)


@login_required(login_url='newfirst') 
def payment(request):
    booking_data = request.session.get('booking_data', {})
    id_r = booking_data.get('id_r')
    seats_r = booking_data.get('seats_r')

    payment_data = request.session.get('payment_data',{})
    source_r = payment_data.get('source_r')
    destination_r = payment_data.get('destination_r')

    if request.method == 'POST':

       booking_data = request.session.get('booking_data', {})
       id_r = booking_data.get('id_r')
       seats_r = booking_data.get('seats_r')

       payment_data = request.session.get('payment_data',{})
       source_r = payment_data.get('source_r')
       destination_r = payment_data.get('destination_r')
  
       bus = Bus.objects.get(id=id_r)
       

       name=request.POST.get('username')
       email=request.POST.get('email')
       age=request.POST.get('age')
       phone=request.POST.get('phone')  
       amount=int(int(seats_r) * bus.price)*100
       client = razorpay.Client(auth=("rzp_test_npyA3ZVuOJNZ4S" , "ffkGSCrGYqUtHLLxLpaXujy0"))

       payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})   
       payment_order_id=payment['id']
       
       en = Registration(
            name=name,
            email=email,
            age=age,
            phone=phone,
            amount=amount,
            order_id=payment_order_id,
       )
       en.save()
        
    #    context={
    #        'amount':amount, 
    #        'api_key':RAZOPAY_API_KEY,
    #        'order_id':payment_order_id
    #    }
       return render(request,'myapp/payment.html',{'payment' : payment,'source_r':source_r,
                     'destination_r':destination_r,'seats_r':seats_r})
       
    return render(request,'myapp/payment.html',{'source_r':source_r,
                     'destination_r':destination_r,'seats_r':seats_r})

@login_required(login_url='newfirst')
@csrf_exempt  
def thank(request):
    dict = {}
    if request.method == "POST":
        a = request.POST
        order_id = ""
        
        for key,val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        user = Registration.objects.filter(order_id=order_id).first()
        user.paid = True
        user.save()
        
        val = int(user.amount)/100
        
        
        # Session data taken from  view.py function
        booking_data = request.session.get('booking_data', {})
        id_r = booking_data.get('id_r')
        seats_r = booking_data.get('seats_r')

        bus = Bus.objects.get(id=id_r)
        
        bus_name = bus.bus_name
        source = bus.source
        dest = bus.dest
        date = bus.date
        time = bus.time


        # Automattically sends the mail
        dicti = {
        'data':user,
        'val':val,
        'bus_name':bus_name,
        'source':source,
        'dest':dest,
        'seats':seats_r,
        'date':date,
        'time':time,
        }

        msg_plain = "YOU HAVE COMPLETED YOUR ADMISSION PROCESS"
        msg_html = render_to_string('myapp/email.html',dicti)

        send_mail("CONGRATULATIONS" ,msg_plain , settings.EMAIL_HOST_USER , [user.email] , html_message = msg_html)

        

       

        name_r = bus.bus_name
        cost = int(seats_r) * bus.price
        source_r = bus.source
        dest_r = bus.dest
        nos_r = Decimal(bus.nos)
        price_r = bus.price
        date_r = bus.date
        time_r = bus.time
        username_r = request.user.username
        email_r = request.user.email
        userid_r = request.user.id

        rem_r = bus.rem - Decimal(seats_r)
        Bus.objects.filter(id=id_r).update(rem=rem_r)

        book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                    source=source_r, busid=id_r,
                                    dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                    status='BOOKED')
        print('------------book id-----------', book.id)

        return render(request, 'myapp/thank.html', locals())

    
    return render(request,"myapp/thank.html",{'id_r': id_r, 'seats_r': seats_r, 'message': 'PAYMENT SUCCESSFUL'})

