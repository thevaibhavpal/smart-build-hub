from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from firstproject.asgi import application
from contractorapp.views import contractorapplications
from .forms import ProjectForm
from homeownerapp.models import*
from contractorapp.models import*
from django.utils import timezone
# Create your views here.
def homeownerdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    if homeowner is None:
        messages.error(request, "User not found.")
        return redirect('login')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
    }
    return render(request, 'homeownerdash.html',context)



    # if not 'homeownerid' in request.session:
    #     messages.error(request,"You are not logged In")
    #     return redirect('login')
    # homeownerid = request.session.get('homeownerid')
    # homeowner = userinfo.objects.filter(email=homeownerid).first()
    
    # context = {
    #     'name': homeowner.name,
    #     'homeownerid': homeownerid,
    # }
    # return render(request, 'homeownerdash.html', context)

def homeownerlogout(request):
    if 'homeowner' in request.session:
        del request.session['homeownerid']
        messages.success(request,"You are logged out")
        return redirect('login')
    else:
        return redirect('login')
    
    
def chpass2(request):
    if not 'homeownerid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('homeownerlogin')
    homeownerid=request.session.get('homeownerid')
    if request.method == 'POST' :
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            homeowner = loginInfo.objects.get(username=homeownerid)
            if homeowner.password != oldpwd:
                messages.error(request,"Old Password is incorrect.")
                return redirect('chpass2')
            elif newpwd != confirmpwd:
                messages.error(request,"New Password and Old Password does not match.")
                return redirect('chpass2')
            elif homeowner.password == newpwd:
                messages.error(request,"The Password is same as old password")
                return redirect('chpass2')
            else:
                homeowner.password = newpwd
                homeowner.save()
                messages.success(request,"Password change successfully")
                return redirect('homeownerdash')
        except loginInfo.DoesNotExist:
                messages.error(request,"Something went wrong")
                return redirect('homeownerlogin')

    return render(request, 'chpass2.html',{'homeownerid':homeownerid})    

def homeownerprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner,
    }
    return render(request, 'homeownerprofile.html',context)

def homeowneredit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner,
    }
    if request.method == 'POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        address=request.POST.get('address')
        bio=request.POST.get('bio')
        profile=request.FILES.get('profile')
        homeowner.name=name
        homeowner.contactno=contactno
        homeowner.address=address
        homeowner.bio=bio
        if profile:
            homeowner.picture=profile
        homeowner.save()
        messages.success(request, "Your profile has been successfully updated")
        return redirect('homeownerprofile')    
    return render(request, 'homeowneredit.html',context)
    


def viewhomeownerproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    projects=Project.objects.filter(homeowner=homeowner)
    if homeowner is None:
        messages.error(request, "User not found.")
        return redirect('login')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request, 'viewhomeownerproject.html',context)

def runninghomeownerproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    project=Project.objects.filter(homeowner=homeowner,status='under_construction')
    
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
    }
    return render(request, 'runninghomeownerproject.html',context)
    
def completehomeownerproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    project=Project.objects.filter(homeowner=homeowner,status='completed')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
    }
    return render(request, 'completehomeownerproject.html',context)


def addhomeownerproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request, "You are not logged In")
        return redirect('login')

    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    form = ProjectForm()
    
    context = {
        'name': homeowner.name,
        'homeownerid': homeownerid,
        'form': form,
    }

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner = homeowner
            project.save()
            messages.success(request, "PROJECT HAS BEEN ADDED")
            return redirect('addhomeownerproject')

    return render(request, 'addhomeownerproject.html', context)


def homeownerviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    project=Project.objects.get(id=id)
    applications=ContractorApplication.objects.filter(project=project)
    
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'applications':applications,
        
    }
    return render(request, 'homeownerviewapplications.html',context)    
    

def rejectapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    app=ContractorApplication.objects.get(id=id)    
    app.status='rejected'
    app.save()
    messages.success(request,"Applications has been rejected")
    return redirect('homeownerviewapplications',id=app.project.id)

def approveapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()
    
    app=ContractorApplication.objects.get(id=id)    
    project=Project.objects.get(id=app.project.id)
    apps=ContractorApplication.objects.filter(project=app.project).update(status='rejected')
    
    app.status='approved'
    app.save()
    project.contractor=app.contractor
    project.start_date=timezone.now()
    project.status='under_construction'
    project.save()
    messages.success(request,"Applications has been approved")
    return redirect('homeownerviewapplications',id=app.project.id)

def viewupdates(request, id):
    if 'homeownerid' not in request.session:
        messages.error(request, "You are not logged In")
        return redirect('login')

    homeownerid = request.session.get('homeownerid')
    homeowner = userinfo.objects.filter(email=homeownerid).first()

    project = Project.objects.filter(id=id).first()  # use .first() to get a single object
    if not project:
        messages.error(request, "Project not found.")
        return redirect('runninghomeownerproject')  # or another appropriate page

    updates = ProgressUpdate.objects.filter(project=project)

    context = {
        'name': homeowner.name,
        'homeownerid': homeownerid,
        'project': project,
        'updates': updates,
    }
    return render(request, 'viewupdates.html', context)



