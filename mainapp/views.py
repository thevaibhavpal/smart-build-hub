from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import requests


# Create your views here.
def index(request):
    return render(request, 'index.html')
def services(request):
    return render(request, 'services.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        enq=Enquiry(email=email,name=name,contactno=contactno,subject=subject,message=message)
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
        "user": "BRIJESH",
        "key": "066c862acdXX",
        "mobile": f"{contactno}",
        "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
        "senderid": "UPDSMS",
        "accusage": "1",
        "entityid": "1201159543060917386",
        "tempid": "1207169476099469445"
}
        response = requests.get(url, params=params)
        print("Response:", response.text)

        messages.success(request,"Your enquiry has been successfully submitted")
        return redirect('contact')
        
    return render(request, 'contact.html')
def login(request):
    return render(request, 'login.html')
def projects(request):
    return render(request, 'projects.html')
def mainbase(request):
    return render(request, 'mainbase.html')
def register(request):
    return render(request, 'register.html')
def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            ad=loginInfo.objects.get(username=username, password=password)
            if ad is not None:
                request.session['adminid']=username
                messages.success(request,"Welcome Admin")
                return redirect('admindash')
            
        except loginInfo.DoesNotExist:
            messages.error(request,"Invalid Credentials")
            return redirect('adminlogin')
        
            
    return render(request, 'adminlogin.html')

def ex(request):
    return render(request, 'ex.html')

def register(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        usertype=request.POST.get('usertype')
        password=request.POST.get('password')
        u=loginInfo.objects.filter(username=email)
        if u:
            messages.error(request, "You already exists")
            return redirect('register')
        log=loginInfo(usertype=usertype,username=email,password=password)
        user=userinfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,'You are successfully registered')
        return redirect('register')
    return render(request, 'register.html')  
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            log = loginInfo.objects.get(username=username,password=password)
            if log.usertype.lower() == "homeowner":
                request.session['homeownerid']=username
                messages.success(request,"welcome Homeowner")
                return redirect('homeownerdash')
            elif log.usertype.lower() == "contractor":
                request.session['contractorid']=username
                messages.success(request,"welcome contractor")
                return redirect('contractordash')
            else:
                messages.error(request,"something went wrong")
                return redirect('contractordash')        
        except loginInfo.DoesNotExist:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request,'login.html')