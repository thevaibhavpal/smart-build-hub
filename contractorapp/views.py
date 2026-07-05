from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from homeownerapp.models import*
from .models import*
from decimal import Decimal

# Create your views here.
def contractordash(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid
    }
    return render(request, 'contractordash.html',context)

def contractorlogout(request):
    if 'contractor' in request.session:
        del request.session['contractorid']
        messages.success(request,"You are logged out")
        return redirect('login')
    else:
        return redirect('login')
    
def chpass1(request):
    if not 'contractorid' in request.session:
        messages.error(request, "You need to login as admin to access this page.")
        return redirect('contractorlogin')
    contractorid=request.session.get('contractorid')
    if request.method == 'POST' :
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            contractor = loginInfo.objects.get(username=contractorid)
            if contractor.password != oldpwd:
                messages.error(request,"Old Password is incorrect.")
                return redirect('chpass1')
            elif newpwd != confirmpwd:
                messages.error(request,"New Password and Old Password does not match.")
                return redirect('chpass1')
            elif contractor.password == newpwd:
                messages.error(request,"The Password is same as old password")
                return redirect('chpass1')
            else:
                contractor.password = newpwd
                contractor.save()
                messages.success(request,"Password changed successfully")
                return redirect('contractordash')
        except loginInfo.DoesNotExist:
                messages.error(request,"Something went wrong")
                return redirect('contractorlogin')

    return render(request, 'chpass1.html',{'contractorid':contractorid})    
    
def contractorprofile(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor,
    }
    return render(request, 'contractorprofile.html',context)

def contractoredit(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'contractor':contractor,
    }
    if request.method == 'POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        address=request.POST.get('address')
        bio=request.POST.get('bio')
        profile=request.FILES.get('profile')
        contractor.name=name
        contractor.contactno=contactno
        contractor.address=address
        contractor.bio=bio
        if profile:
            contractor.picture=profile
        contractor.save()
        messages.success(request, "Your profile has been successfully updated")
        return redirect('contractorprofile')    
    return render(request, 'contractoredit.html',context)
    


def contractorviewprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    projects=Project.objects.filter(contractor=None)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'projects':projects
    }
    return render(request, 'contractorviewprojects.html',context)


from decimal import Decimal  # Ensure this import is present at the top

def applyproject(request, id):
    if not 'contractorid' in request.session:
        messages.error(request, "You are not logged In")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)

    context = {
        'name': contractor.name,
        'contractorid': contractorid,
        'project': project
    }

    application = ContractorApplication.objects.filter(project=project, contractor=contractor)
    if application.exists():
        messages.warning(request, "You have already applied for this project")
        return redirect('contractorviewprojects')

    if request.method == 'POST':
        proposal_text = request.POST.get('proposal_text')
        design_file = request.FILES.get('design_file')
        estimated_budget_str = request.POST.get('estimated_budget')  # Fix here

        try:
            estimated_budget = Decimal(estimated_budget_str)  # Convert safely
        except:
            messages.error(request, "Invalid estimated budget")
            return redirect('applyproject', id=id)  # Stay on form page if error

        estimated_duration = request.POST.get('estimated_duration')

        app = ContractorApplication(
            contractor=contractor,
            project=project,
            proposal_text=proposal_text,
            design_file=design_file,
            estimated_budget=estimated_budget,
            estimated_duration=estimated_duration
        )
        app.save()
        messages.success(request, "Project Application submitted successfully")
        return redirect('contractorviewprojects')

    return render(request, 'applyproject.html', context)


def contractorapplications(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    applications=ContractorApplication.objects.filter(contractor=contractor)
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'applications':applications
    }
    return render(request, 'contractorapplications.html',context)

def assignedproject(request):
    if not 'contractorid' in request.session:
        messages.error(request,"You are not logged In")
        return redirect('login')
    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    project=Project.objects.filter(contractor=contractor)
    
    context = {
        'name':contractor.name,
        'contractorid':contractorid,
        'project':project
    }
    return render(request, 'assignedproject.html',context)


def addprogress(request, id):
    if 'contractorid' not in request.session:
        messages.error(request, "You are not logged In")
        return redirect('login')

    contractorid = request.session.get('contractorid')
    contractor = userinfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)

    context = {
        'name': contractor.name,
        'contractorid': contractorid,
        'project': project
    }

    if request.method == 'POST':
        update_text = request.POST.get('update_text')
        image = request.FILES.get('image')
        progress_percent = request.POST.get('progress_percent')

        # ✅ Validate update_text
        if not update_text or update_text.strip() == "":
            messages.error(request, "Update text is required.")
            return redirect('addprogress', id=id)

        try:
            progress_percent = int(progress_percent)
        except (TypeError, ValueError):
            messages.error(request, "Invalid progress percentage")
            return redirect('addprogress', id=id)

        if progress_percent > 100:
            messages.error(request, "Progress cannot be more than 100%")
            return redirect('addprogress', id=id)

        elif progress_percent < 0:
            messages.error(request, "Progress cannot be less than 0%")
            return redirect('addprogress', id=id)

        elif progress_percent < project.progress:
            messages.error(request, "Progress cannot be less than current progress")
            return redirect('addprogress', id=id)

        # ✅ Now it's safe to create and save
        pu = ProgressUpdate(
            project=project,
            update_text=update_text,
            image=image,
            progress_percent=progress_percent,
            updated_by=contractor
        )

        project.progress = progress_percent
        if progress_percent == 100:
            project.status = 'completed'

        project.save()
        pu.save()

        messages.success(request, "Progress updated successfully")
        return redirect('assignedproject')

    return render(request, 'addprogress.html', context)




