from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm,SetPasswordForm
from .forms import Extradata, EditUserData
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from full_user import settings
from django.core.mail import send_mail,EmailMessage #to send email
from django.contrib.sites.shortcuts import get_current_site #why we used it?
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token



# Create your views here.
def Signup(request):
    if request.method == 'POST':
        fm = Extradata(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            f_name = fm.cleaned_data['first_name']
            l_name = fm.cleaned_data['last_name']
            username = fm.cleaned_data['username']
            pass1 = fm.cleaned_data['password1']
            # pass2 = fm.cleaned_data['password2']
            if User.objects.filter(email=email):
                messages.error(request,'Email already Existed ! Please try some other Email Address')
                return redirect('Signup')
            store = User(first_name=f_name,last_name=l_name,email=email,username=username)
            store.set_password(pass1) #esse hi humara password store ho sakta h User model wala..
            store.is_active = False #till user not verified his account via email
            store.save()
            messages.success(request,'User Created Successfully')
            # if User.objects.filter(username=username):
            #     messages.error(request,'Username already Existed ! Please try some other Username')
            #     return redirect('Signup')

            #Welcome Email
            Subject = 'Welcome to my new project'
            message = 'Hello' + store.first_name +'!! \n' + 'welcome to our Email project! \n.we will never contact you or store your email in our database.Please confirm your email adress..'
            from_email = settings.EMAIL_HOST_USER
            to_list = [store.email]
            send_mail(Subject,message,from_email,to_list,fail_silently = True) #import send_mail() from django.core.mail import send_mail

            #Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = 'Confirm your email @ CFG - Django Login!!'
            message2 = render_to_string('full/email_confirmation.html',
            {
                'name':store.first_name,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(store.pk)),
                'token':generate_token.make_token(store)
            })
            email = EmailMessage(email_subject,message2,settings.EMAIL_HOST_USER,[store.email])
            email.fail_silently = True
            email.send()
            messages.success(request,'Hello User!, Confirmation Email has been send to your Email id.')
            return redirect('login')
    else:
        fm = Extradata()
        fm.order_fields(field_order=['first_name','last_name','username','email','password1','password2'])
    return render(request,'full/Signup.html',{'form':fm})

def login1(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return redirect('profile')
                else:
                    messages.success(request,'Entered Password not matched with old Password')
                    # return redirect('login')
        else:
            fm=AuthenticationForm()
        return render(request,'full/login.html',{'form':fm})
    else:
        return redirect('profile')
    
def profile(request):
    if request.user.is_authenticated:  #only view profile when you are logined
        if request.method == 'POST':    
            fm = EditUserData(request.POST,instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Data Modified Successfully')
        else:
            fm = EditUserData(instance=request.user)
        return render(request,'full/profile.html',{'form':fm})
    else:
        return redirect('login')

def logout1(request):
    logout(request)
    return redirect('login')

def password2(request):  #This takes only New password..
    if request.method == 'POST':
        fm = SetPasswordForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,'Password changed successfully')
            return redirect('profile')
    else:
        fm = SetPasswordForm(user=request.user)
    return render(request,'full/profile.html',{'forms':fm})


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        store = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        store = None

    if store is not None and generate_token.check_token(store,token):
        store.is_active = True
        store.save()
        login(request,store)
        return redirect('login')
    else:
        return HttpResponse('Error In validation.')


