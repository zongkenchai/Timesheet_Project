from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import MyUser


# Create your forms here.

class NewUserForm(UserCreationForm):

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.fields["user_name"].widget.attrs.update({
			'placeholder': 'Allison Imrie',
			'type' : "username",
			'class' : "form-control mb-4", 
			'id':"username"
		})
		self.fields["email"].widget.attrs.update({
			'placeholder': 'example@uwa.edu.au',
			'type' : "email",
			'class' : "form-control mb-4",
			'id' : "email "
		})
		
		self.fields["password1"].widget.attrs.update({
			'type' : "password",
			'class' : "form-control mb-4",
			'id' : "password",
			'placeholder' : "Password"
		})

		self.fields["password2"].widget.attrs.update({
			'type' : "confirm_password ",
			'class' : "form-control mb-4",
			'id' : "confirm_password",
			'placeholder' : "Confirm Password"
		})

	email = forms.EmailField(required=True)

	class Meta:
		model = MyUser
		fields = ("user_name", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		# user.is_email_verified = True
		if commit:
			user.save()
		return user