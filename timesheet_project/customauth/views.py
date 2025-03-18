import email
from email import message
from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from user_registration.models import RegisteredEmail
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this

from django.contrib.auth import authenticate, login, logout

from .forms import NewUserForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from .utils import generate_token

from django.core.mail import EmailMessage
from django.conf import settings
from .models import MyUser
# from  django.utils.encoding import force_text

# force_text = force_str

def send_activation_email(user, request):
	current_site = get_current_site(request)

	email_subject = 'Activate your Account'
	email_body = render_to_string('registration/activate.html', {
		'user': user,
		'domain': current_site,
		'uid' : urlsafe_base64_encode(force_bytes(user.email)),
		'token' : generate_token.make_token(user)
	})

	email = EmailMessage(subject=email_subject, body=email_body, from_email = settings.EMAIL_FROM_USER, to = [user.email])

	email.send()

def register_request(request):

	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.is_email_verified = False

			# votes_table = Votes.objects.filter(user_id=user_id, post_id= post_id).exists()

			all_emails = RegisteredEmail.objects.all()

			present = False
			if all_emails is not None:
				for each in all_emails:
					# print(each.email_address)
					if user.email == each.email_address:
						present = True
						break
			
			if not present:
				messages.error(request, "Provided email address is not permitted to register, please contact admin!")
				form = NewUserForm()
				return render(request=request, template_name="signup.html", context={"form":form})


			# login(request, user)

			# messages.success(request, "Registration successful." )

			send_activation_email(user, request)
			from django.contrib import messages

			messages.success(request, "Please check your inbox and click on the activation link to activate your account!")
			user.save()
			return redirect("homepage")

			# else:
			# 	messages.success(request, "Email not permitted!")
			# 	return redirect("register")
		else:
			return render(request, 'signup.html', context={"form":form})

	else:
		# messages.error(request, "Unsuccessful registration. Invalid information.")
		form = NewUserForm()
		return render(request=request, template_name="signup.html", context={"form":form})



# def login_request(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request, data=request.POST)
# 		if form.is_valid():
# 			# email = form.cleaned_data.get('email')
# 			# password = form.cleaned_data.get('password')
# 			email = request.POST['email']
# 			password = request.POST['password']
# 			user = authenticate(request, email=email, password=password)
# 			if user is not None:
# 				login(request, user)
# 				messages.info(request, f"You are now logged in as {user.user_name}.")
# 				return redirect("homepage")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 				return redirect("login")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="registration/login.html", context={"login_form":form})


# def login_user(request):

# 	if request.method == 'POST':
# 		context = {'data': request.POST}
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		user = authenticate(request, username=username, password=password)

# 		if not user:
# 			messages.add_message(request, messages.ERROR, 'Invalid credentials, try again!')
# 			return render(request, 'registration/login.html', context, status=401)

# 		login(request, user)

# 		messages.add_message(request, messages.SUCCESS, f'Welcome {user.username}')

# 		return redirect(reverse('home'))
	
# 	return render(request, 'registration/login.html')

def login_request(request):

	if request.method == 'POST':
		context = {'data': request.POST}
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(email=email, password=password)
		
		# if user.is_email_verified:
		# 	messages.add_message(request, messages.ERROR, 'Email is not verified')
		# 	return render(request, 'registration/login.html', context)
		current_user = MyUser.objects.filter(email=email)
		if len(current_user)==1:
			if not current_user[0].is_email_verified and not current_user[0].is_admin:
				messages.add_message(request, messages.ERROR, 'Email is not verified')
				return render(request, 'registration/login.html', context)

		if not user:
			messages.add_message(request, messages.ERROR, 'Invalid credentials, try again!')
			return render(request, 'registration/login.html', context, status=401)



		login(request, user)

		messages.add_message(request, messages.SUCCESS, f'Welcome {user}')

		return redirect(reverse('homepage'))
	
	return render(request, 'registration/login.html')

# def login_user(request):
# 	return render(request, "registration/login.html")

def homepage(request):
	# return render(request, "landing.html")
	return redirect('dashboard')


def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser._default_manager.get(email=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()

        messages.success(request, "Email verified, you can now login")  # ✅ Use Django's messaging

        return redirect(reverse("homepage"))  # ✅ Redirect to homepage after success
    else:
        return render(request, "registration/activation-failed.html", {"user": user})