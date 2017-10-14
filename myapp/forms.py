from django import forms
from django.contrib.auth import get_user_model

from .models import City, Category, Entry, Review

User = get_user_model()


class CityForm(forms.ModelForm):
	class Meta:
		model = City
		fields = ['name', 'image_url', 'description']


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['type', 'image_url']


class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['phone', 'name', 'address', 'image_url']


class NewEntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['city', 'category', 'phone', 'name', 'address', 'image_url']


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		# fields = ['user', 'entry', 'rating', 'review']

		fields = ['rating', 'review']


class NewReviewForm(forms.ModelForm):
	class Meta:
		model = Review

		fields = ['entry', 'rating', 'review']

	# def __init__(self, *args, **kwargs):
	# 	entry = kwargs.pop('entry', None)
	# 	user = kwargs.pop('user', None)
	# 	super(ReviewForm, self).__init__(*args, **kwargs)
	# 	entry_object = Entry.objects.get(slug=str(entry))
	# 	self.initial['entry'] = entry_object.pk
	# 	self.fields['entry'].disabled = True
	# 	self.initial['user'] = user
	# 	self.fields['user'].disabled = True


class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


	class Meta:
		model = User
		fields = ('username', 'email',)


	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email__iexact=email)
		if qs.exists():
			raise forms.ValidationError("Email already exists")
		return email



	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.is_active = False
		# create a new user hash for activating email.

		if commit:
			user.save()
			user.infouser.send_activation_email()
		return user
