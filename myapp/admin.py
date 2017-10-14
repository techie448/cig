from django.contrib import admin
from .models import City, Category, Entry, Review, InfoUser

# Register your models here.
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Entry)
admin.site.register(Review)
admin.site.register(InfoUser)
