from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import auth, User
from .models import Blogs,Newsmodel,Fertilizermodel,Expertsmodel,Company,AppointmentScheduleModel
from django.contrib import messages
# Create your views here.
import random
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.files import File
import datetime

def index(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    iscompany=False
    try:
        company=Company.objects.get(email=request.user.email)
        if(company):
            iscompany=True
        else:
            iscompany=False
    except:
        iscompany=False
    allfertilizer=Fertilizermodel.objects.all()
     
    serialized_data = []
    for p in allfertilizer:
        whichuser=""
        if p.user.is_superuser:
            whichuser="Admin"
        else:
            whichuser=p.user.username
        serialized_data.append({"user":whichuser,"title":p.title,"description":p.description,"media":p.media,})
    print(serialized_data)
    return render(request,"home.html",{"allfertilizer":allfertilizer,"iscompany":iscompany})

def logout(request):
    auth.logout(request)
    return redirect("/login")



def blogs(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    iscompany=False
    try:        
        company=Company.objects.get(email=request.user.email)
        if(company):
            iscompany=True
        else:
            iscompany=False
    except:
        iscompany=False
    allBlogs=Blogs.objects.all()
     
    serialized_data = []
    for p in allBlogs:
        whichuser=""
        if p.user.is_superuser:
            whichuser="Admin"
        else:
            whichuser=p.user.username
        serialized_data.append({"title":p.title,"description":p.description,"user":whichuser,"media":p.media})
    print(serialized_data)
    return render(request,"blogs.html",{"allBlogs":serialized_data,"iscompany":iscompany})

def AddBlogs(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    iscompany=False
    try:
        company=Company.objects.get(email=request.user.email)
        if(company):
            iscompany=True
        else:
            iscompany=False
    except:
        iscompany=False
    if request.method == "POST":
        title = request.POST.get("blogtitle")
        print(request.FILES)
        fileimg = request.FILES["blogfile"]
        print(fileimg,"files")
        convertedFile=File(fileimg, name=fileimg)
        description = request.POST.get("blogdescription")
        newblog = Blogs(title=title,description=description,user=request.user,media=fileimg)
        newblog.save()
        messagesBlog ="Successfully Added A New Blog {}".format(title)
        messages.add_message(request, 159, messagesBlog)
        return render(request,"addblogs.html",{"iscompany":iscompany})
    return render(request,"addblogs.html",{"iscompany":iscompany})

def AddFertilizer(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    iscompany=False
    try:
        company=Company.objects.get(email=request.user.email)
        if(company):
            iscompany=True
        else:
            iscompany=False
    except:
        iscompany=False
    if request.method == "POST":
        title = request.POST.get("fertilizertitle")
        print(request.FILES)
        fileimg = request.FILES["fertilizerfile"]
        print(fileimg,"files")
        convertedFile=File(fileimg, name=fileimg)
        description = request.POST.get("fertilizerdescription")
        rating = request.POST.get("fertilizerrating")
        newfertilizer = Fertilizermodel(title=title,description=description,user=request.user,media=fileimg,rating=rating)
        newfertilizer.save()
        messagesBlog ="Successfully Added A New Fertilizer {}".format(title)
        messages.add_message(request, 159, messagesBlog)
        return render(request,"addfertilizer.html",{"iscompany":iscompany})
    return render(request,"addfertilizer.html",{"iscompany":iscompany})


def login(request):
    if request.method == "POST":
        Username = request.POST.get("Username")
        Password = request.POST.get("Password")
        user = auth.authenticate(username=Username, password=Password)
        if user is not None:
            auth.login(request, user)
            greetings = [
                f"Hello @{user.username}, Welcome back",
                f"Hi there @{user.username},Glad you came back",
                f"Hi there @{user.username},It's good to see you again"
            ]
            messages.add_message(request, 159, random.choices(greetings)[0])
            return HttpResponseRedirect("/")
        else:
            message = "Invalid Email or Password"
            messages.add_message(
                request, 951, "Couldn't Login, Invalid Username or Password")
            return render(request, "login.html")
    else:
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "login.html")
def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["Username"])
            if user is not None:
                E_message = f"Invalid username: {user} already taken"
                messages.add_message(request, 951, E_message)
                return render(request, "reg.html")

        except User.DoesNotExist:
            
            Username = request.POST["Username"]
            Password = request.POST["Password"]
            email = request.POST["email"]
            ConfirmPassword = request.POST["ConfirmPassword"]
            accountType = "user"
            try:
                getAccountType=request.POST["companyaccount"]
                accountType="company"
                if Password == ConfirmPassword:
                    user = User.objects.create_user(
                        email=email,
                        username=Username,
                        password=Password,
                        first_name=Username,
                    )
                    user.save()
                    company=Company(email=email,
                        username=Username,
                        password=Password,
                        first_name=Username.split(" ")[0],company=Username).save()
                    messg = f"Company {user} registered successfully"
                    messages.add_message(request, 159, messg)
                    user = auth.authenticate(username=Username, password=Password)
                    return redirect("/")
                else:
                    message = "Password are not same"
                    messages.add_message(request, 951, message)
                    return render(request, "reg.html")
            except:
                print("failed first")
                accountType="user"
                if Password == ConfirmPassword:
                    user = User.objects.create_user(
                        email=email,
                        username=Username,
                        password=Password,
                        first_name=Username,
                    )
                    user.save()
                    messg = f"User {user} registered successfully"
                    messages.add_message(request, 159, messg)
                    user = auth.authenticate(username=Username, password=Password)
                    return redirect("/")
                else:
                    message = "Password are not same"
                    messages.add_message(request, 951, message)
                    return render(request, "reg.html")
    else:
        return render(request, "reg.html")
def News(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    iscompany=False
    try:
        company=Company.objects.get(email=request.user.email)
        if(company):
            iscompany=True
        else:
            iscompany=False
    except:
        iscompany=False
    allnews=Newsmodel.objects.all()
     
    serialized_data = []
    for p in allnews:
         serialized_data.append({"title":p.title,"description":p.description,"media":p.media})
    print(serialized_data)
    return render(request,"news.html",{"allnews":serialized_data,"iscompany":iscompany})

def Experts(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    elif request.method=="POST":
        title = request.POST["appointmentTitle"]
        description = request.POST["appointmentDesc"]
        expertEmail=request.POST["expertEmail"]
        dateofappointment=request.POST["datepicker"]
        findExpert=Expertsmodel.objects.get(email=expertEmail)
        newfertilizer = AppointmentScheduleModel(title=title,description=description,farmer=request.user,expert=findExpert,appointmentDate=dateofappointment)
        newfertilizer.save()
        send_mail(
    'Appointment Requested',
    "An appointment Is requested,\n\nBy Farmer: {}\nEmail:{}\nDate:{}\n\nWith Following Details:\n\n Title: {}\nDescription:{}\n".format(request.user.username,request.user.email,dateofappointment,title,description),
    'organicfertilizer91@gmail.com',
    [expertEmail],
    fail_silently=False,
)
        

    iscompany=False
    try:
        company=Company.objects.get(email=request.user.email)
        if(company):
            iscompany=True
        else:
            iscompany=False
    except:
        iscompany=False
    allexperts=Expertsmodel.objects.all()
    
    serialized_data = []
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
    for p in allexperts:
        serialized_data.append({"email":p.email,"title":p.name,"description":p.description,"media":p.avtar,"contact":p.contact,"rating":range(p.rating),"nonRating":range(5-p.rating)})
    print(serialized_data)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request,"experts.html",{"curdate":current_datetime,"allexperts":serialized_data,"iscompany":iscompany})

def Fertilizer(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    iscompany=False
    try:
        company=Company.objects.get(email=request.user.email)
        if(company):
            iscompany=True
        else:
            iscompany=False
    except:
        iscompany=False
    allfertilizer=Fertilizermodel.objects.all()
     
    serialized_data = []
    for p in allfertilizer:
        whichuser=""
        if p.user.is_superuser:
            whichuser="Admin"
        else:
            whichuser=p.user.username
        serialized_data.append({"user":whichuser,"title":p.title,"description":p.description,"media":p.media,"rating":range(p.rating),"nonRating":range(5-p.rating)})
    print(serialized_data)
    return render(request,"fertilizer.html",{"allfertilizer":serialized_data,"iscompany":iscompany})

