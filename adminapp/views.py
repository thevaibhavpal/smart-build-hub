from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from homeownerapp.models import*
from contractorapp.models import*
from django.views.decorators.cache import cache_control
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('adminlogin')
    
    adminid=request.session.get('adminid')
    context={
        'adminid':adminid,
        'th':userinfo.objects.filter(login__usertype="homeowner").count(),
        'tc':userinfo.objects.filter(login__usertype="contractor").count(),
        'tp':Project.objects.all().count(),
        'trp':Project.objects.filter(status='under_construction').count(),
        'tcp':Project.objects.filter(status='completed').count(),
    }
    return render(request,'admindash.html',context)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, "You are logged out")
        return redirect('adminlogin')
    else:
        return redirect('index')
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    enqs=Enquiry.objects.all()
    return render(request, 'viewenq.html',{'enqs':enqs,'adminid':adminid})
def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('adminlogin')
    enq=Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,"Enquiry delete successfully")
    return redirect('viewenq')


def chpass(request):
    if not 'adminid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    if request.method == 'POST' :
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            admin = loginInfo.objects.get(username=adminid)
            if admin.password != oldpwd:
                messages.error(request,"Old Password is incorrect.")
                return redirect('chpass')
            elif newpwd != confirmpwd:
                messages.error(request,"New Password and Old Password does not match.")
                return redirect('chpass')
            elif admin.password == newpwd:
                messages.error(request,"The Password is same as old password")
                return redirect('chpass')
            else:
                admin.password = newpwd
                admin.save()
                messages.success(request,"Password change successfully")
                return redirect('admindash')
        except loginInfo.DoesNotExist:
                messages.error(request,"Something went wrong")
                return redirect('adminlogin')

    return render(request, 'chpass.html',{'adminid':adminid})

def managecontractors(request):
    if not 'adminid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('adminlogin')
    
    adminid=request.session.get('adminid')
    contractors = userinfo.objects.filter(login__usertype='contractor')
    return render(request, 'managecontractors.html',{'adminid':adminid, 'contractors': contractors})


def managehomeowners(request):
    if not 'adminid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('adminlogin')
    
    adminid = request.session.get('adminid')
    homeowners = userinfo.objects.filter(login__usertype='homeowner')
    return render(request, 'managehomeowners.html', {'adminid': adminid, 'homeowners': homeowners})

def blockcontractor(request, id):
    contractor = userinfo.objects.get(id=id)
    contractor.is_active = False
    contractor.save()
    messages.success(request, "Contractor blocked successfully.")
    return redirect('managecontractors')

def unblockcontractor(request, id):
    contractor = userinfo.objects.get(id=id)
    contractor.is_active = True
    contractor.save()
    messages.success(request, "Contractor unblocked successfully.")
    return redirect('managecontractors')

def blockhomeowner(request, id):
    homeowner = userinfo.objects.get(id=id)
    homeowner.is_active = False
    homeowner.save()
    messages.success(request, "Homeowner blocked successfully.")
    return redirect('managehomeowners')

def unblockhomeowner(request, id):
    homeowner = userinfo.objects.get(id=id)
    homeowner.is_active = True
    homeowner.save()
    messages.success(request, "Homeowner unblocked successfully.")
    return redirect('managehomeowners')






