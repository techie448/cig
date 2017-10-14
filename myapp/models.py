from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.core.mail import send_mail
from .validators import clean_image_url
from .utils import code_generator
User = settings.AUTH_USER_MODEL


# Create your models here.

class InfoUser(models.Model):
	user = models.OneToOneField(User)
	activated = models.BooleanField(null=False, blank=False, default=False)
	activation_key = models.CharField(max_length=120, blank=True, null=True)

	def __str__(self):
		return self.user.username

	def send_activation_email(self):
		pass
		if not self.activated:
			self.activation_key = code_generator()  # 'somekey' #gen key
			self.save()
			# path_ = reverse()
			path_ = reverse('myapp:activate', kwargs={"code": self.activation_key})
			subject = 'Activate Account'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = f'Activate your account here: {path_}'
			recipient_list = [self.user.email]
			html_message = f'<p>Activate your account here: {path_}</p>'
			print(html_message)
			sent_mail = send_mail(
			                subject,
			                message,
			                from_email,
			                recipient_list,
			                fail_silently=False,
			                html_message=html_message)


			# subject = 'Activate Account'
			# from_email = settings.DEFAULT_FROM_EMAIL
			# message = f'Activate your account here {self.activation_key}'
			# recipient_list = [self.user.email]
			# html_message = f'<h1>Actyivate your account here : {self.activation_key}</h1>'
			#
			# send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
			sent_mail = False
			return sent_mail


class City(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=250, unique=True,
	                        validators=[RegexValidator('^[a-zA-Z ]+$', message='Only Alphabets')])
	image_url = models.URLField(max_length=500, validators=[clean_image_url])
	description = models.TextField()
	slug = models.SlugField(null=False, blank=False, unique=True)

	class Meta:
		ordering = ['name']

	def get_absolute_url(self):
		return reverse('myapp:admin-city')

	def __str__(self):
		return self.name


class Category(models.Model):
	user = models.ForeignKey(User)
	type = models.CharField(max_length=250, unique=True,
	                        validators=[RegexValidator('^[a-zA-Z ]+$', message='Only Alphabets')])
	image_url = models.URLField(max_length=500, validators=[clean_image_url])
	slug = models.SlugField(null=False, blank=False, unique=True)

	def __str__(self):
		return self.type

	@staticmethod
	def get_absolute_url():
		return reverse('myapp:admin-category')

	class Meta:
		ordering = ['type']


class Entry(models.Model):
	user = models.ForeignKey(User)
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=250,
	                        validators=[RegexValidator('^[A-Za-z0-9 ]+$', message='Only Alphanumeric Characters')])
	phone = models.CharField(max_length=10, validators=[
		RegexValidator('^[0-9]{10,10}$', message='Enter a 10 digit phone number without area code')])
	address = models.CharField(max_length=250)
	image_url = models.URLField(max_length=500, validators=[clean_image_url])
	avg_rating = models.DecimalField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True,
	                                 max_digits=3, decimal_places=1)
	slug = models.SlugField(null=False, blank=False, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		category = self.category.slug
		city = self.city.slug
		return reverse('myapp:entry', kwargs={'city': city, 'category': category})

	class Meta:
		unique_together = ('city', 'category', 'name')
		ordering = ['city']


class Review(models.Model):
	user = models.ForeignKey(User)
	entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
	rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	review = models.TextField(validators=[RegexValidator('^[A-Za-z0-9 ]+$', message='Only Alphanumeric Characters')])
	slug = models.SlugField(null=False, blank=False, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		print("i am here")
		entry = self.entry.slug
		entry_obj = get_object_or_404(Entry, slug=entry)
		city = entry_obj.city.slug
		category = entry_obj.category.slug
		print("here")
		return reverse('myapp:review', kwargs={'city': city, 'category': category, 'entry': entry})

	def __str__(self):
		return str(self.rating)

	class Meta:
		unique_together = ('user', 'entry')
		ordering = ['-date_updated']


def pre_save_city(sender, instance, *args, **kwargs):
	instance.name = instance.name.title()
	if not instance.slug:
		instance.slug = slugify(instance.name)


def pre_save_category(sender, instance, *args, **kwargs):
	instance.type = instance.type.title()
	if not instance.slug:
		instance.slug = slugify(instance.type)


def pre_save_entry(sender, instance, *args, **kwargs):
	instance.name = instance.name.title()
	if not instance.slug:
		city = instance.city
		category = instance.category
		instance.slug = slugify(instance.name + str(city.pk) + str(category.pk))


def pre_save_review(sender, instance, *args, **kwargs):
	if not instance.slug:
		entry = instance.entry
		user = instance.user
		unique_id = get_random_string(length=8)
		instance.slug = slugify(str(entry.pk) + str(user.pk) + '-' + str(unique_id))


def set_avg_rating(sender, instance, *args, **kwargs):
	if instance.rating:
		print("hllli")
		# obj = get_list_or_404(Review, entry=instance.entry)
		obj = Review.objects.filter(entry=instance.entry)
		print('abc')
		total = 0
		count = len(obj) + 1
		for i in obj:
			total += i.rating
		avg = total / count
		avg = round(avg, 1)
		print('aaaaa')
		obj2 = get_object_or_404(Entry, pk=instance.entry.pk)
		obj2.avg_rating = avg
		obj2.save()
		print('zzzzz')


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		is_created = InfoUser.objects.get_or_create(user=instance)


pre_save.connect(pre_save_category, sender=Category)
pre_save.connect(pre_save_entry, sender=Entry)
pre_save.connect(pre_save_review, sender=Review)
post_save.connect(pre_save_review, sender=Review)
pre_save.connect(pre_save_city, sender=City)
pre_save.connect(set_avg_rating, sender=Review)
post_delete.connect(set_avg_rating, sender=Review)
post_save.connect(post_save_user_receiver, sender=User)
