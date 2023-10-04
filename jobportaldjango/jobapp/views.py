from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Admin  # Import your Admin model
from .forms import AdminProfileUpdateForm, AdminPasswordResetForm  # Create these forms
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Notification,JobPosting
from .forms import JobSearchForm
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
    return render(request, "index.html")
def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Applicant.objects.get(user=user)
                if user1.type == "applicant":
                    login(request, user)
                    return redirect("/user_homepage")
                else:
                    return render(request, "user_login.html")
      
            else:
                thank = True
                return render(request, "user_login.html", {'thank':thank})
    return render(request, "user_login.html")   

def signup(request):
    if request.method=="POST":   
        username = request.POST['email']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']      
        phone = request.POST['phone']
        gender = request.POST['gender']
        image = request.FILES['image']
        if User.objects.filter(username=username).exists(): 
            messages.info(request, "username already exist")
        elif User.objects.filter(email=email).exists():
            messages.info(request, "email already exist")
        else:           
            subject = 'newuser' 
            r=''
            for i in range(6):
                r= r+str(random.randint(0,9))
            message = f'hello {first_name} {last_name} your registration has been completed successfully. And you temporary password will be {r}thank you'     
            send_mail(subject, 
                message, settings.EMAIL_HOST_USER, [email])
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,password=r)
            applicants = Applicant.objects.create(user=user, phone=phone, gender=gender, image=image, type="applicant")
            user.save()
            applicants.save()
            return render(request, "user_login.html")
    return render(request, "signup.html")   

def user_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/user_login/')
    applicant = Applicant.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.save()
        applicant.user.save()

        try:
            image = request.FILES['image']
            applicant.image = image
            applicant.save()
        except:
            pass
        alert = True
        user_id = request.session.get('user_id')
        if user_id:
            user = Applicant.objects.get(pk=user_id)
        
            if not user.is_profile_complete:
               messages.info(request, 'Please complete your profile to apply for jobs.')
    
        return render(request, "user_homepage.html", {'alert':alert})
    return render(request, "user_homepage.html", {'applicant':applicant})
# def user_homepage(request):
#     user_id = request.session.get('user_id')
#     if user_id:
#         user = Applicant.objects.get(pk=user_id)
        
#         if not user.is_profile_complete:
#             messages.info(request, 'Please complete your profile to apply for jobs.')
    
#     return render(request, 'user_homepage.html')
def all_jobs(request):
    jobs = Job.objects.all().order_by('-start_date')
    applicant = Applicant.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "all_jobs.html", {'jobs':jobs, 'data':data})
def job_detail(request, myid):
    job = Job.objects.get(id=myid)
    return render(request, "job_detail.html", {'job':job})
def job_apply(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    applicant = Applicant.objects.get(user=request.user)
    job = Job.objects.get(id=myid)
    date1 = date.today()
    if job.end_date < date1:
        closed=True
        return render(request, "job_apply.html", {'closed':closed})
    elif job.start_date > date1:
        notopen=True
        return render(request, "job_apply.html", {'notopen':notopen})
    else:
        if request.method == "POST":
            resume = request.FILES['resume']
            Application.objects.create(job=job, company=job.company, applicant=applicant, resume=resume, apply_date=date.today())
            alert=True
            return render(request, "job_apply.html", {'alert':alert})
    return render(request, "job_apply.html", {'job':job})        
def Logout(request):
    logout(request)
    return redirect('index')
def company_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            user1 = Company.objects.get(user=user)
            if user1.type == "company" and user1.status == "pending":
                login(request, user)
                return redirect("/company_homepage")
            else:
                return render(request, "company_login.html")
        else:
            alert = True
            return render(request, "company_login.html", {"alert":alert})

    return render(request, "company_login.html")
def company_signup(request):
    if request.method=="POST":   
        username = request.POST['username']
        email1 = request.POST['email']
        first_name1=request.POST['first_name']
        last_name1=request.POST['last_name']
        
        phone = request.POST['phone']
        gender = request.POST['gender']
        image = request.FILES['image']
        company_name = request.POST['company_name']
        if User.objects.filter(username=username).exists(): 
            messages.info(request, "username already exist")
        elif User.objects.filter(email=email1).exists():
            messages.info(request, "email already exist")
        else:  
            subject = 'newemployer' 
            r=''
            for i in range(6):
                r= r+str(random.randint(0,9))
            message = f'hello {first_name1} {last_name1} your registration has been completed successfully. And you temporary password will be {r}thank you'     
            send_mail(subject, 
                message, settings.EMAIL_HOST_USER, [email1])
            
            
            user = User.objects.create_user(is_staff=1,first_name=first_name1, last_name=last_name1, email=email1, username=username,password=r)
            company = Company.objects.create(user=user, phone=phone, gender=gender, image=image, company_name=company_name, type="company", status="pending")
            user.save()
            company.save()
            return render(request, "company_login.html")
    return render(request, "company_signup.html")
def company_homepage(request):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    company = Company.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        company.user.email = email
        company.user.first_name = first_name
        company.user.last_name = last_name
        company.phone = phone
        company.gender = gender
        company.save()
        company.user.save()

        try:
            image = request.FILES['image']
            company.image = image
            company.save()
        except:
            pass
        alert = True
        return render(request, "company_homepage.html", {'alert':alert})
    return render(request, "company_homepage.html", {'company':company})
def add_job(request):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        description = request.POST['description']
        user = request.user
        company = Company.objects.get(user=user)
        job = Job.objects.create(company=company, title=title, type=type,start_date=start_date, end_date=end_date, salary=salary, image=company.image, experience=experience, location=location, skills=skills, description=description, creation_date=date.today())
        job.save()
        alert = True
        return render(request, "add_job.html", {'alert':alert})
    return render(request, "add_job.html")
def job_list(request):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    companies = Company.objects.get(user=request.user)
    jobs = Job.objects.filter(company=companies)
    return render(request, "job_list.html", {'jobs':jobs})
def all_applicants(request):
    company = Company.objects.get(user=request.user)
    application = Application.objects.filter(company=company)
    return render(request, "all_applicants.html", {'application':application})
def edit_job(request, myid):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    job = Job.objects.get(id=myid)
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        description = request.POST['description']

        job.title = title
        job.salary = salary
        job.experience = experience
        job.location = location
        job.skills = skills
        job.description = description

        job.save()
        if start_date:
            job.start_date = start_date
            job.save()
        if end_date:
            job.end_date = end_date
            job.save()
        alert = True
        return render(request, "edit_job.html", {'alert':alert})
    return render(request, "edit_job.html", {'job':job})

def company_logo(request, myid):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    job = Job.objects.get(id=myid)
    if request.method == "POST":
        image = request.FILES['logo']
        job.image = image 
        job.save()
        alert = True
        return render(request, "company_logo.html", {'alert':alert})
    return render(request, "company_logo.html", {'job':job})
def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user.is_superuser:
            login(request, user)
            return redirect("/all_companies")
        else:
            alert = True
            return render(request, "admin_login.html", {"alert":alert})
    return render(request, "admin_login.html")
def all_companies(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    companies = Company.objects.all()
    return render(request, "all_companies.html", {'companies':companies})
def view_applicants(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    applicants = Applicant.objects.all()
    return render(request, "view_applicants.html", {'applicants':applicants})
def change_status(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    company = Company.objects.get(id=myid)
    if request.method == "POST":
        status = request.POST['status']
        company.status=status
        company.save()
        alert = True
        return render(request, "change_status.html", {'alert':alert})
    return render(request, "change_status.html", {'company':company})
def accepted_companies(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    companies = Company.objects.filter(status="Accepted")
    return render(request, "accepted_companies.html", {'companies':companies})
def pending_companies(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    companies = Company.objects.filter(status="pending")
    return render(request, "pending_companies.html", {'companies':companies})
def rejected_companies(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    companies = Company.objects.filter(status="Rejected")
    return render(request, "rejected_companies.html", {'companies':companies})
def delete_company(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    company = User.objects.filter(id=myid)
    company.delete()
    return redirect("/all_companies")
def delete_applicant(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    applicant = User.objects.filter(id=myid)
    applicant.delete()
    return redirect("/view_applicants")
def admin_dashboard(request):
    # Retrieve lists of employers and job seekers
    employers = Company.objects.all()
    jobseekers = Applicant.objects.all()

    return render(request, 'admin_dashboard.html', {'employers': employers, 'jobseekers': jobseekers})
def common_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_superuser==1 and user.is_staff==1:
                    login(request,user)
                    # return redirect("/all_companies")
                    return redirect("admin_profile_update")

                elif user.is_superuser==0 and user.is_staff==1:
                    login(request, user)
                    return redirect("company_homepage")
                elif user.is_superuser==0 and user.is_staff==0:
                    login(request, user)
                    return redirect("/user_homepage")                               
            else:
               
                return render(request, "common_login.html")
    return render(request, "common_login.html")   

def newlogin(request):
    return render(request,'common_login.html')
# def reset_password(request):
#     return render(request,'resetpass.html')
# def newpassword(request,pk):
#     password1 = request.POST['password1']
#     password2 = request.POST['password2']

def reset_password(request):
    return render(request,'base.html')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def password_change_done(request):
    return render(request, 'password_change_done.html')    
# Admin Profile Update View
class AdminProfileUpdateView(UpdateView):
    model = Admin
    form_class = AdminProfileUpdateForm
    template_name = 'admin_profile_update.html'
    success_url = reverse_lazy('admin_profile_update_success')  # Create a success URL

# Admin Password Reset View
class AdminPasswordResetView(PasswordChangeView):
    form_class = AdminPasswordResetForm
    template_name = 'admin_password_reset.html'
    success_url = reverse_lazy('admin_password_reset_success')  # Create a success URL
# @login_required
# def admin_profile_update(request):
#     admin = request.user.admin  # Assuming 'admin' is the related name for the Admin model in User
#     if request.method == 'POST':
#         form = AdminProfileUpdateForm(request.POST, instance=admin)
#         if form.is_valid():
#             form.save()
#             return redirect('profile_updated')  # Redirect to a success page
#     else:
#         form = AdminProfileUpdateForm(instance=admin)
#     return render(request, 'admin_profile_update.html', {'form': form})

def admin_profile_update(request):
    if request.method == 'POST':
        user_form = AdminProfileUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was successfully updated.')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = AdminProfileUpdateForm(instance=request.user)
    return render(request, 'admin_profile_update.html', {'user_form': user_form})
@login_required
def admin_password_reset(request):
    if request.method == 'POST':
        form = AdminPasswordResetForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to keep the user logged in after a password change
            update_session_auth_hash(request, user)
            return redirect('password_reset_done')  # Redirect to a success page
    else:
        form = AdminPasswordResetForm(request.user)
    return render(request, 'admin_password_reset.html', {'form': form})
@staff_member_required
def verify_profile(request, profile_type, profile_id):
    if profile_type == 'employer':
        profile = Company.objects.get(id=profile_id)
    elif profile_type == 'jobseeker':
        profile = Applicant.objects.get(id=profile_id)
    else:
        # Handle invalid profile_type
        return redirect('admin_dashboard')  # Redirect to admin dashboard or an error page

    # Toggle the is_verified field
    profile.is_verified = not profile.is_verified
    profile.save()

    # Redirect back to admin dashboard or the page you prefer
    return redirect('admin_dashboard')
def admin_panel(request):
    employers = Company.objects.all()
    jobseekers = Applicant.objects.all()
    return render(request, 'admin_panel.html', {'employers': employers, 'jobseekers': jobseekers})
def block_profile(request, profile_type, profile_id):
    if profile_type == 'employer':
        try:
            employer_profile = Company.objects.get(id=profile_id)
            # Toggle the is_blocked field
            employer_profile.is_blocked = not employer_profile.is_blocked
            employer_profile.save()
        except Company.DoesNotExist:
            # Handle the case where the EmployerProfile doesn't exist
            pass  # You can redirect to an error page or handle it as needed
    elif profile_type == 'jobseeker':
        try:
            jobseeker_profile = Applicant.objects.get(id=profile_id)
            # Toggle the is_blocked field
            jobseeker_profile.is_blocked = not jobseeker_profile.is_blocked
            jobseeker_profile.save()
        except Applicant.DoesNotExist:
            # Handle the case where the JobSeekerProfile doesn't exist
            pass  # You can redirect to an error page or handle it as needed
    else:
        # Handle invalid profile_type
        pass  # You can redirect to an error page or handle it as needed

    # Redirect back to the admin panel or the page you prefer
    return redirect('admin_panel')

def remove_profile(request, profile_type, profile_id):
    if profile_type == 'employer':
        Company.objects.filter(id=profile_id).delete()
    elif profile_type == 'jobseeker':
        Applicant.objects.filter(id=profile_id).delete()
    else:
        # Handle invalid profile_type
        return redirect('admin_panel')  # Redirect to admin panel or an error page

    # Redirect back to admin panel or the page you prefer
    return redirect('admin_panel')
def job_application_count(request):
    # Query the Job model and annotate it with the count of related JobApplications
    jobs = Job.objects.annotate(application_count=Count('application'))
    
    return render(request, 'job_application_count.html', {'jobs': jobs})

def employer_register(request):
    if request.method == 'POST':
        # Handle employer registration form submission
        # Create a new employer user
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        
        # Create a notification for the admin
        notification = Notification(user=User.objects.get(username='admin'), message=f'New employer registration: {user.username}')
        notification.save()
        
        # Log in the new employer user
        login(request, user)
        
        return redirect('company_homepage')  # Redirect to employer's dashboard

    return render(request, 'company_signup.html')

def job_seeker_register(request):
    if request.method == 'POST':
        # Handle job seeker registration form submission
        # Create a new job seeker user
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        
        # Create a notification for the admin
        notification = Notification(user=User.objects.get(username='admin'), message=f'New job seeker registration: {user.username}')
        notification.save()
        
        # Log in the new job seeker user
        login(request, user)
        
        return redirect('user_homepage')  # Redirect to job seeker's dashboard

    return render(request, 'signup.html')
def approve_profile(request, user_id):
    user = User.objects.get(id=user_id)
    # Approve the user's profile (e.g., set is_verified=True)
    user.profile.is_verified = True
    user.profile.save()
    # Mark the notification as read
    notification = Notification.objects.get(user=request.user, message=f'New user registration: {user.username}')
    notification.is_read = True
    notification.save()
    return redirect('admin_dashboard')

def disapprove_profile(request, user_id):
    user = User.objects.get(id=user_id)
    # Disapprove the user's profile (e.g., delete the user)
    user.delete()
    # Mark the notification as read
    notification = Notification.objects.get(user=request.user, message=f'New user registration: {user.username}')
    notification.is_read = True
    notification.save()
    return redirect('admin_dashboard')
# def admin_nofifications(request):
#     employers = Company.objects.all()
#     jobseekers = Applicant.objects.all()

#     return render(request, 'admin_notifications.html', {'admin_notifications': employers, 'admin_notifications': jobseekers})
@login_required
def admin_notifications(request):
    # Retrieve lists of employers and job seekers
    employers = User.objects.filter(groups__name='company')
    job_seekers = User.objects.filter(groups__name='applicant')
    notifications = Notification.objects.filter(is_read=False)
    
    if request.method == 'POST':
        # Handle admin's approval or disapproval action here
        # You can update the user profiles accordingly
        
        # Mark the notifications as read after action
        notifications.update(is_read=True)
        return redirect('admin_notifications')

    return render(request, 'admin_notifications.html', {'employers': employers, 'job_seekers': job_seekers, 'notifications': notifications})

@login_required
def admin_job_approval(request):
    if request.user.is_staff:
        pending_jobs = JobPosting.objects.filter(is_approved=False)
        if request.method == 'POST':
            # Handle job approval/disapproval here
            job_id = request.POST['job_id']
            is_approved = request.POST['is_approved'] == '1'
            job = JobPosting.objects.get(id=job_id)
            job.is_approved = is_approved
            job.save()

            # Create a notification for the employer
            message = f'Your job posting "{job.title}" has been {"approved" if is_approved else "disapproved"}.'
            notification = Notification(user=job.employer, message=message)
            notification.save()

            return redirect('admin_job_approval')

        return render(request, 'admin_job_approval.html', {'pending_jobs': pending_jobs})
    else:
        return redirect('user_homepage')

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
        
#         if authenticated:
#             request.session['user_id'] = user.id  # Store the user's ID in the session
#             return redirect('user_homepage')
#         else:
#             messages.error(request, 'Invalid login credentials')
    
#     return render(request, 'login.html')
def job_search(request):
    jobs = Job.objects.all()
    search_form = JobSearchForm(request.GET)

    if search_form.is_valid():
        location = search_form.cleaned_data.get('location')
        job_name = search_form.cleaned_data.get('job_name')
        job_type = search_form.cleaned_data.get('job_type')

        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_name:
            jobs = jobs.filter(title__icontains=job_name)      
        if job_type:
            jobs = jobs.filter(job_type=job_type)

    return render(request, 'job_search.html', {'jobs': jobs, 'search_form': search_form})

def seeker_profiles(request):
    # Query the SeekerProfile model to get a list of seekers
    seekers = Applicant.objects.all()  # You should adjust this query as needed

    # Render the HTML template and pass the list of seekers to it
    return render(request, 'user_homepage.html', {'seekers': seekers})
# def applied_jobs(request):
    
#      status_filter = request.GET.get('status', 'all')
    
#      if status_filter == 'all':
#          user_profile = Applicant.objects.get(user=request.user)

#          applications = Application.objects.filter(applicant=user_profile)
   
#         # applications = Application.objects.filter(applicant=request.user)
#      else:
#         applications = Application.objects.filter(applicant=request.user, status=status_filter)
    
#      return render(request, 'applied_jobs.html', {'applications': applications, 'status_filter': status_filter})


def applied_jobs(request):
    user = request.user

    # Check if the user is an applicant (assuming you have different user types)
    try:
        applicant = Applicant.objects.get(user=user)
    except Applicant.DoesNotExist:
        applicant = None

    # Get the status_filter from the GET request
    status_filter = request.GET.get('status', 'all')

    # Filter the applications based on the status_filter and the applicant
    if applicant and status_filter != 'all':
        applications = Application.objects.filter(applicant=applicant, status=status_filter)
    elif applicant:
        applications = Application.objects.filter(applicant=applicant)
    else:
        applications = []

    return render(request, 'applied_jobs.html', {'applications': applications, 'status_filter': status_filter})



def change_application_status(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    applicant = Applicant.objects.get(id=myid)
    if request.method == "POST":
        status = request.POST['status']
        applicant.status=status
        applicant.save()
        alert = True
        return render(request, "change_status.html", {'alert':alert})
    return render(request, "change_status.html")

def accept_job(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        # Your logic to accept the job

        # Notify the user about the accepted job
        messages.success(request, f'You have accepted the job: {job.title}')

        # Pass further information as context data
        context = {
            'job': job,
            'additional_info': 'This is additional information about the job.',
        }

        return render(request, 'job_detailnew.html', context)

    except Job.DoesNotExist:
        return redirect('all_jobs')

def dashboard(request):
    # Job statistics
    job_count = Job.objects.count()
    scheduled_jobs = Job.objects.filter(schedule__isnull=False).count()

    # Calculate the date one week ago
    one_week_ago = datetime.now() - timedelta(days=7)

    # Recent job postings in the last week
    recent_jobs = Job.objects.filter(created_at__gte=one_week_ago)

    # Applicant count for each job
    jobs_with_applicant_count = Job.objects.annotate(applicant_count=Count('application'))

    context = {
        'job_count': job_count,
        'scheduled_jobs': scheduled_jobs,
        'recent_jobs': recent_jobs,
        'jobs_with_applicant_count': jobs_with_applicant_count,
    }

    return render(request, 'dashboard.html', context)


def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notification_list.html', {'notifications': notifications})

def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    notification.is_read = True
    notification.save()
    return render(request, 'notification_detail.html', {'notification': notification})


   

